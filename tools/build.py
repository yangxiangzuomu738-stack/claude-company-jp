"""agency-agents の原文から日本版の担当者ファイルと担当者一覧を作る。

    git clone --depth 1 https://github.com/msitarzewski/agency-agents <作業フォルダ>
    python -I tools/build.py <作業フォルダ>

- 担当者の名前と説明は tools/names-ja.tsv と tools/roles-ja.tsv から付ける。
- tools/japan/ にある担当者は、中国市場向けの原文の代わりに日本向けに書き直したものを使う。
- 出力: agents/<部門>/jp-*.md と skills/claude-company-jp/references/担当者一覧.md
"""
import csv
import json
import pathlib
import re
import shutil
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
TOOLS = REPO / "tools"
OUT = REPO / "agents"
ROSTER = REPO / "skills" / "claude-company-jp" / "references" / "担当者一覧.md"

# 元の部門 -> 日本版のフォルダ
DIVISIONS = {
    "finance": "01-経理",
    "sales": "02-営業",
    "marketing": "03-マーケティング",
    "paid-media": "04-広告運用",
    "product": "05-企画",
    "project-management": "06-進行管理",
    "support": "07-サポート",
    "testing": "08-テスト",
    "design": "09-デザイン",
    "engineering": "10-エンジニアリング",
    "security": "11-セキュリティ",
    "specialized": "12-専門職",
    "academic": "13-学術・リサーチ",
    "research": "13-学術・リサーチ",
    "game-development": "14-ゲーム開発",
    "gis": "15-地図・GIS",
    "healthcare": "16-医療",
    "spatial-computing": "17-空間コンピューティング",
}

HEADER = """# {jp}（英語名: {en}）

## 日本版での働き方

- 返答と成果物はすべて日本語で書く。
- 下の本文は agency-agents の英語の原文。役割・手順・品質の基準は本文に従う。
- 法律・税・会計・労務・広告・個人情報などは日本の制度を基準にする。本文が米国など他の国の制度を前提にしているところは日本の制度に読み替え、読み替えられないときはその旨を書く。制度の情報は国税庁・厚生労働省・消費者庁・個人情報保護委員会・e-Gov 法令検索などの公的な資料で確かめ、出典を書く。
- 金額は円、日付は年月日で書く。
- 送信・投稿・公開・購入・支払い・本番への反映など外に出る操作は、依頼者の許可を取ってから行う。許可がなければ下書きまでにする。

## 英語の原文

"""

DROP_KEYS = {"name", "description", "emoji", "vibe"}


def read_tsv(path, key, value):
    with open(path, encoding="utf-8", newline="") as f:
        return {r[key]: r[value] for r in csv.DictReader(f, delimiter="\t")}


def split_front(text):
    _, fm, body = text.split("---", 2)
    return fm.strip("\n"), body.lstrip("\n")


def front_value(fm, key):
    m = re.search(rf"^{key}:\s*(.+)$", fm, re.M)
    return m.group(1).strip().strip('"') if m else None


def kept_lines(fm):
    keep, skipping = [], False
    for line in fm.splitlines():
        m = re.match(r"^([A-Za-z_-]+):", line)
        if m:
            skipping = m.group(1) in DROP_KEYS
        if not skipping:
            keep.append(line)
    return keep


def yaml_str(s):
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    src = pathlib.Path(sys.argv[1])
    names = read_tsv(TOOLS / "names-ja.tsv", "name", "jp_name")
    roles = read_tsv(TOOLS / "roles-ja.tsv", "name", "ja")
    japan = {p.name: p for p in (TOOLS / "japan").glob("*.md")}

    if OUT.exists():
        shutil.rmtree(OUT)
    rows, missing, used = [], [], set()
    divs = list(json.load(open(src / "divisions.json", encoding="utf-8"))["divisions"].keys())
    for div in divs:
        for p in sorted((src / div).rglob("*.md")):
            text = p.read_text(encoding="utf-8")
            if not text.startswith("---"):
                continue
            fm, body = split_front(text)
            en = front_value(fm, "name")
            if not en:
                continue
            folder = OUT / DIVISIONS[div]
            folder.mkdir(parents=True, exist_ok=True)
            target = folder / f"jp-{p.name}"
            if p.name in japan:
                jtext = japan[p.name].read_text(encoding="utf-8")
                jfm, _ = split_front(jtext)
                jp, desc = front_value(jfm, "name"), front_value(jfm, "description")
                target.write_text(jtext, encoding="utf-8")
                kind = "日本向けに書き直し"
            else:
                if en not in names or en not in roles:
                    missing.append(en)
                    continue
                jp, desc = names[en], f"{roles[en]}。英語版の {en}（agency-agents）の日本版。"
                lines = ["---", f"name: {jp}", f"description: {yaml_str(desc)}", *kept_lines(fm), "---", "", ""]
                target.write_text("\n".join(lines) + HEADER.format(jp=jp, en=en) + body, encoding="utf-8")
                kind = ""
            if jp in used:
                sys.exit(f"日本語名が重複: {jp}")
            used.add(jp)
            rows.append((DIVISIONS[div], jp, desc, en, kind, target.relative_to(REPO).as_posix()))
    if missing:
        sys.exit("names-ja.tsv か roles-ja.tsv にない担当者: " + ", ".join(missing))
    unused = set(japan) - {pathlib.PurePosixPath(r[5]).name[3:] for r in rows}
    if unused:
        sys.exit("tools/japan に使われていないファイル: " + ", ".join(sorted(unused)))

    write_roster(rows)
    print(f"担当者 {len(rows)}人（日本向けに書き直し {len(japan)}人）")


def write_roster(rows):
    lines = [
        "# 担当者一覧",
        "",
        f"全{len(rows)}人。Agent ツールの subagent_type には「名前」をそのまま渡す。",
        "「日本向け」は、中国市場向けだった原文を日本の媒体・制度向けに書き直した担当者。",
        "",
    ]
    for folder in sorted({r[0] for r in rows}):
        group = sorted((r for r in rows if r[0] == folder), key=lambda r: r[1])
        lines += [f"## {folder[3:]}（{len(group)}人）", "", "| 名前 | 役割 | 英語名 |", "|---|---|---|"]
        for _, jp, desc, en, kind, path in group:
            role = desc.split("。")[0]
            mark = "（日本向け）" if kind else ""
            lines.append(f"| [{jp}](../../../{path}){mark} | {role} | {en} |")
        lines.append("")
    ROSTER.parent.mkdir(parents=True, exist_ok=True)
    ROSTER.write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    main()
