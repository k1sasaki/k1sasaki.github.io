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
