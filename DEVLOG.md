# DEVLOG

## 2026-10-18 Calypso移行・favicon差し替え・海保ジンラミー掲載

claude.aiでの相談(2026-10-13〜18、Cowork君)からClaude Codeに引き継いで開始。

- Calypso `~/projects/aramono_ten/` にリポジトリを作成。`github`(push用SSH)・`nas`(`/mnt/repos/aramono_ten.git`)の2リモート構成に。GitHub Codespaceは廃止。
- 公開の流れを確立し、READMEに明記:ローカル確認 → `git push github draft` → PR相当の内容をdraft→mainへマージ(ここで公開)→ 本番確認 → `git push nas --all`。
- Codespaceに未送信のまま残っていた分(favicon.ico/png/apple-touch-icon.png、goods/_template、新README)をDownloadsから回収してCalypsoに取り込み、公開。
- 全ページにdev-badge(`assets/dev-badge.js`):本番ホスト名以外ではタブタイトルに🔧を付けて、手元プレビューと本番を見分けられるように。
- 新しい商品ページ `goods/rummy1/`(海保ジンラミー、Rummy1 Calypso:3106の紹介)を作成・公開。要相談(お取り寄せ)系の商品の型として、雛形に「直リンクなしバージョン」のコメント例を追記。
- `assets/style.css` に `.shot` / `.shot img` の修正(`max-width:100%` / `width:100%; height:auto;`)。画面写真の解像度・縦横比がバラバラでも、トリミングを気にせずそのまま使えるように。
- meta description と og:description は内容を変える(descriptionは検索結果向けにきちんと、og:descriptionは共有カード向けに短く)方針に決め、雛形のプレースホルダーも書き換え済み。

**次回の予定:** 部品差し込みツール(includer)を作る。`<!-- include: 名前 -->`〜`<!-- /include: 名前 -->` の目印の中身を、部品フォルダのファイルで差し替える、汎用のPythonスクリプト。まずヘッダーとお問い合わせURLの重複解消に使う想定。マーカーは実行後も残るので、部品を直せば何度でも再実行できる設計にする。

## 2026-10-19 includer実装・波高し returns掲載・ロゴバッジ

- `tools/includer.py` を実装。`parts/header.html`・`parts/head-assets.html` を部品化し、既存4ページに目印コメントを追加(表示内容は不変)。目印が0または1組以外ならエラーで止まり書き込まない安全弁つき。実際にheaderの文言を書き換えて4ページへ伝播する実地テストも実施(確認後に復元)。
- 新しい商品ページ `goods/namitakashi_llm/`(波高し returns、Rails/Calypso:3108の紹介)を作成・公開。rummy1と同じく直リンクなし(要相談)。画面写真5枚(①名前登録→②海域選択→③配備→④開戦→⑤決着)を店主が撮影して提供。
- 各アプリ自身のロゴ(512×512アイコン等)を商品ページのh1横に出す `.product-title` パターンを追加(雛形にもコメントで記載)。白地・線画で寂しく見えるロゴ用に、縦長・緑縁の `.karuta` バリアントも追加(bicycle-rule-drillの自転車ロゴに適用)。
- card.png([16:10]棚カード画像)を、画面写真をそのまま流用して中身が変な位置で切れる失敗を2回(rummy1・namitakashi_llm)経験。原因は`object-fit: cover`で16:10以外の比率の画像を使うと上下左右が機械的に切れること。店主が16:10に近い比率で撮り直す運用に。
- プレビュー中、ブラウザがassets/style.cssを古いままキャッシュする問題に複数回遭遇(CSSを直してもpython3 -m http.serverの中身は正しいのに表示が変わらない)。`link.href`にクエリを足して強制再読み込みで都度確認。

**次回の予定:** 海保ジンラミーの「あなたが使うと、こう働きます」を、店主の娘さんのエピソード(マリウスには勝てるが本当の相手には勝てない。無駄な手を切り詰める・配牌の良さを逃さない、が勝ち筋)を使って書き直す。残りの商品(句集づくり・ドラマトラッカー・Movie Clipper・おかしな英会話・EasyWriter)は未着手。
