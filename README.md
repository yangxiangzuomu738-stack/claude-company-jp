# Claude会社（日本版）

Claude Code を「会社」として動かすためのスキルと、日本語で働く283人の担当者のセットです。

あなたが社長、Claude が社長室長です。頼んだ仕事に合う担当者（経理・営業・マーケティング・デザイン・開発・テストなど17部門）を Claude が選んで任せ、結果を確かめてから日本語で報告します。

- 担当者の名前はすべて日本語です（例：経理・記帳担当、LINE公式アカウント運用担当、UIデザイナー）。
- 担当者は日本語で答え、法律・税・労務・広告は日本の制度で考えます。
- 送信・投稿・支払いなど外に出る操作は、あなたの許可なしには行いません。
- 元になったのは [msitarzewski/agency-agents](https://github.com/msitarzewski/agency-agents)（MIT ライセンス）です。中国市場向けの22人は、日本の媒体・制度向けに書き直しました。

## 入れ方（Claude Code の中で2行）

Claude Code の入力欄に、次の2行を1行ずつ打ちます。

```text
/plugin marketplace add yangxiangzuomu738-stack/claude-company-jp
```

```text
/plugin install claude-company-jp@claude-company-jp
```

入れ終わると、そのセッションのまますぐ使えます。「Run /reload-plugins to apply.」と表示されたときは、続けて `/reload-plugins` と打ちます。Claude Code を開き直す必要はありません。

ターミナルから入れる場合は次の2行です。この場合は、次に Claude Code を開いたときから使えます。

```bash
claude plugin marketplace add yangxiangzuomu738-stack/claude-company-jp
```

```bash
claude plugin install claude-company-jp@claude-company-jp
```

プラグインで入れると、担当者の名前の前に `claude-company-jp:` が付きます（例: `claude-company-jp:経理・記帳担当`）。頼むときは付けなくてもかまいません。

### 更新・外し方（プラグイン）

```text
/plugin marketplace update claude-company-jp
```

```text
/plugin uninstall claude-company-jp@claude-company-jp
```

## 別の入れ方（ファイルをコピーする）

プラグインを使わずに `~/.claude` へ直接コピーしたいときの方法です。担当者の名前の前に何も付きません。Python 3.8 以上と Git が必要です。

```bash
git clone https://github.com/yangxiangzuomu738-stack/claude-company-jp.git
cd claude-company-jp
python install.py
```

Windows で `python` が見つからないときは `py install.py` を使います。

| 入るもの | 場所 |
|---|---|
| スキル `claude-company-jp` | `~/.claude/skills/claude-company-jp/` |
| 担当者283人 | `~/.claude/agents/jp-*.md` |

同じ名前のファイルが既にあるときは上書きしません。上書きしたいときは `python install.py --force`、外すときは `python install.py --uninstall` を使います。

## 使い方

Claude Code にふつうに頼むだけです。「会社で」「〇〇担当に任せて」と書くと、確実にこのスキルが使われます。

```text
会社で、新しいカフェの開店に向けた LINE公式アカウントの運用計画を作って
```

```text
提案書担当と価格設定担当に、この見積もりの見直しを任せて
```

```text
このリポジトリをコードレビュー担当とAI生成コード安全監査担当にチェックさせて
```

担当者を名指しして直接呼ぶこともできます。

```text
経理・記帳担当として、この試算表の気になる点を挙げて
```

## 部門と担当者

全283人の名前・役割・英語名は [担当者一覧](skills/claude-company-jp/references/担当者一覧.md) にあります。

| 部門 | 人数 | 主な担当者 |
|---|---|---|
| [経理](agents/01-経理) | 5 | 経理・記帳担当、予算・予実管理担当、税務担当 |
| [営業](agents/02-営業) | 9 | 提案書担当、ヒアリング設計担当、新規開拓担当 |
| [マーケティング](agents/03-マーケティング) | 37 | LINE公式アカウント運用担当、note運用担当、口コミ・UGC担当、日本語SEO・MEO担当 |
| [広告運用](agents/04-広告運用) | 7 | 検索広告担当、SNS広告担当、計測・タグ設定担当 |
| [企画](agents/05-企画) | 6 | プロダクトマネージャー、市場トレンド調査担当 |
| [進行管理](agents/06-進行管理) | 7 | シニアプロジェクトマネージャー、議事録担当 |
| [サポート](agents/07-サポート) | 6 | 問い合わせ対応担当、分析レポート担当 |
| [テスト](agents/08-テスト) | 9 | テスト自動化担当、最終品質判定担当 |
| [デザイン](agents/09-デザイン) | 10 | UIデザイナー、UXアーキテクト、UI仕上げ審査担当 |
| [エンジニアリング](agents/10-エンジニアリング) | 66 | 試作担当、コードレビュー担当、LINEミニアプリ開発担当 |
| [セキュリティ](agents/11-セキュリティ) | 12 | AI生成コード安全監査担当、秘密情報管理担当 |
| [専門職](agents/12-専門職) | 59 | 社長室長、経営戦略担当、自治体・官公庁提案担当、採用担当 |
| [学術・リサーチ](agents/13-学術・リサーチ) | 7 | 文献調査担当、統計の専門家 |
| [ゲーム開発](agents/14-ゲーム開発) | 21 | ゲームデザイナー、Unity設計担当 |
| [地図・GIS](agents/15-地図・GIS) | 13 | GISアナリスト、Web地図開発担当 |
| [医療](agents/16-医療) | 3 | 医療エビデンス担当 |
| [空間コンピューティング](agents/17-空間コンピューティング) | 6 | visionOS開発担当 |

### 日本向けに書き直した22人

| 日本版 | 元の担当（中国向け） |
|---|---|
| LINE公式アカウント運用担当 | Private Domain Operator（WeChat 法人版） |
| note運用担当 | WeChat Official Account Manager |
| 口コミ・UGC担当 | Xiaohongshu Specialist（小紅書） |
| ネット世論・炎上対策担当 | Weibo Strategist（微博） |
| Q&A・専門知識発信担当 | Zhihu Strategist（知乎） |
| 動画コミュニティ担当 | Bilibili Content Strategist |
| ショート動画横断担当 | Douyin Strategist（抖音） |
| 地域密着発信担当 | Kuaishou Strategist（快手） |
| ライブコマース担当 | Livestream Commerce Coach |
| ブログ一括下書き担当 | Multi-Platform Publisher |
| 日本の音声配信担当 | Podcast Strategist |
| 日本語SEO・MEO担当 | Baidu SEO Specialist |
| 国内ECモール運営担当 | China E-Commerce Operator |
| 日本市場ローカライズ担当 | China Market Localization Strategist |
| 国内企業ネットワーク担当 | China Network Engineer |
| 国内業務ツール連携担当 | Feishu Integration Developer |
| LINEミニアプリ開発担当 | WeChat Mini Program Developer |
| 自治体・官公庁提案担当 | Government Digital Presales Consultant |
| 医療・健康広告の法規制担当 | Healthcare Marketing Compliance Specialist |
| 採用担当 | Recruitment Specialist |
| 調達・取引適正化担当 | Supply Chain Strategist |
| 留学相談担当 | Study Abroad Advisor |

ほかの261人は、日本語の名前・役割と「日本語で答え、日本の制度で考える」という指示を冒頭に足し、本文は英語の原文のままです。

## 自分の会社の決まりを足す

`~/.claude/CLAUDE.md` に決まりを書いておくと、Claude が担当者への依頼文に入れます。たとえば次のように書きます。

```markdown
## 会社の決まり
- 資料に絵文字を使わない
- 金額は税込で書く
- freee への登録は必ず私が確認してから
```

## フォルダの中身

```text
claude-company-jp/
├── README.md                      この説明
├── .claude-plugin/                プラグインとマーケットプレイスの設定
├── install.py                     ファイルをコピーして入れる・外すスクリプト
├── LICENSE                        MIT ライセンス
├── skills/claude-company-jp/
│   ├── SKILL.md                   社長室長の手順（振り分け・依頼文・会社の決まり）
│   └── references/担当者一覧.md    全283人の一覧
├── agents/                        担当者283人（部門ごとのフォルダ）
└── tools/                         担当者ファイルを作り直すための材料
    ├── build.py
    ├── names-ja.tsv               日本語の名前
    ├── roles-ja.tsv               日本語の役割
    └── japan/                     日本向けに書き直した22人の原稿
```

## ライセンス

MIT ライセンスです。担当者の本文は [msitarzewski/agency-agents](https://github.com/msitarzewski/agency-agents)（Copyright (c) 2025 AgentLand Contributors、MIT）の原文を使っています。詳しくは [LICENSE](LICENSE) を見てください。
