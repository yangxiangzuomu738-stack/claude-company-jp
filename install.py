"""Claude会社（日本版）を Claude Code に入れる・外す。

    python install.py              # スキルと担当者283人を入れる（同名のファイルは上書きしない）
    python install.py --force      # 同名のファイルも上書きする
    python install.py --uninstall  # このスクリプトで入れたものを外す

入れる場所:
    スキル   ~/.claude/skills/claude-company-jp/
    担当者   ~/.claude/agents/jp-*.md
"""
import argparse
import pathlib
import shutil
import sys

REPO = pathlib.Path(__file__).resolve().parent
SKILL_NAME = "claude-company-jp"
MANIFEST = "claude-company-jp-installed.txt"


def install(root, force):
    skill_src = REPO / "skills" / SKILL_NAME
    skill_dest = root / "skills" / SKILL_NAME
    agents_dest = root / "agents"
    agents_dest.mkdir(parents=True, exist_ok=True)

    if skill_dest.exists():
        shutil.rmtree(skill_dest)
    shutil.copytree(skill_src, skill_dest)

    files = sorted(REPO.glob("agents/*/jp-*.md"))
    copied, skipped = [], 0
    for p in files:
        target = agents_dest / p.name
        if target.exists() and not force:
            skipped += 1
            continue
        shutil.copy2(p, target)
        copied.append(p.name)

    manifest = agents_dest / MANIFEST
    known = set(manifest.read_text(encoding="utf-8").split()) if manifest.exists() else set()
    manifest.write_text("\n".join(sorted(known | set(copied))) + "\n", encoding="utf-8")

    print(f"スキル: {skill_dest}")
    print(f"担当者: {len(files)}人中 {len(copied)}人を入れました（既にあった {skipped}人はそのまま） -> {agents_dest}")
    print("新しいセッションから使えます。")


def uninstall(root):
    agents_dest = root / "agents"
    manifest = agents_dest / MANIFEST
    removed = 0
    if manifest.exists():
        for name in manifest.read_text(encoding="utf-8").split():
            target = agents_dest / name
            if target.exists():
                target.unlink()
                removed += 1
        manifest.unlink()
    skill_dest = root / "skills" / SKILL_NAME
    if skill_dest.exists():
        shutil.rmtree(skill_dest)
    print(f"担当者 {removed}人とスキルを外しました。")


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description="Claude会社（日本版）を入れる・外す")
    ap.add_argument("--force", action="store_true", help="同名のファイルも上書きする")
    ap.add_argument("--uninstall", action="store_true", help="入れたものを外す")
    ap.add_argument("--root", default=str(pathlib.Path.home() / ".claude"), help="入れる先（既定: ~/.claude）")
    args = ap.parse_args()
    root = pathlib.Path(args.root).expanduser()
    if args.uninstall:
        uninstall(root)
    else:
        install(root, args.force)


if __name__ == "__main__":
    main()
