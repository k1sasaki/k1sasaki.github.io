# 佐々木IT粗物店(Sasaki Peopleware Works)

https://k1sasaki.github.io/ で公開する店のサイトです。

## 置き方

このフォルダの中身を、リポジトリ `k1sasaki/k1sasaki.github.io` の一番上にそのまま置きます。
GitHub の Settings → Pages で「Deploy from a branch」、ブランチ `main`、フォルダ `/ (root)` を選ぶと公開されます。

## 中身

- `index.html` … 店先(トップページ)
- `goods/<商品名>/index.html` … 商品ページ(`goods/bicycle-rule-drill/` が型)
- `assets/style.css` … 全ページ共通のデザイン
- `assets/favicon.svg` … タブのアイコン
- `.nojekyll` … GitHub の変換処理を止めて、ファイルをそのまま公開するための空ファイル

## 商品を足すとき

1. `index.html` の `<article class="card">` を1つ複製して書き換える
2. 商品ページを作るなら `goods/bicycle-rule-drill/` をフォルダごと複製して書き換える

札の種類:`tag-stock`(店頭在庫あり)、`tag-order`(お取り寄せ)、`tag-soon`(入荷予定)、`tag-done`(販売終了)

## 注意

既存のアプリ(`bicycle-rule-drill` など)は別のリポジトリなので、このサイトを置いても URL は変わりません。
