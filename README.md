# 佐々木IT粗物店(Sasaki Peopleware Works)

https://k1sasaki.github.io/ で公開している店のサイトです。

## フォルダの中身

```
index.html                 店先(トップページ)
assets/
  style.css                全ページ共通のデザイン(色・文字・並べ方)
  favicon.ico, favicon.png,
  apple-touch-icon.png    タブ/ホーム画面のアイコン(四つ菱)
  storefront-wide.jpg      店先の写真
  og-image.jpg             トップを共有したときの画像
goods/
  _template/index.html     商品ページの雛形(複製して使う)
  bicycle-rule-drill/      商品ページの見本
    index.html
    card.html              棚に出すカードの中身(商品名・一言・リンクなど)
    card.png               棚のカード・共有用(横長 16:10)
    shot-1.png …           画面写真(使う順)
tools/
  build_shelf.py           shelf-order.txt の順に card.html を集めて棚を組み立てる
  includer.py              ヘッダーなど共通部分を部品化して差し込む
parts/
  header.html, head-assets.html   共通部分の部品(includer.py が使う)
shelf-order.txt            棚の並び順・「一押し」区分
.nojekyll                  ファイルをそのまま公開するための空ファイル
```

- 1ページ = 1フォルダ + その中の `index.html`。URL はフォルダ名で決まる。
- 店全体の画像は `assets/`、商品の画像はその商品のフォルダ。
- ファイル名は半角の英小文字・数字・ハイフンだけ。

## 商品ページの作り方

1. `goods/_template` を複製し、フォルダ名を商品の英字名にする(アプリのURLと同じ名前がよい)。
2. 画面写真を同じフォルダに置く。`card.png`(横長 16:10)と `shot-1.png`、`shot-2.png` …(使う順)。
3. `index.html` の【 】を埋める。Ctrl+F で「【」を検索して、残りがなくなるまで。
4. `noindex` の1行と、先頭の説明コメントを消す。
5. 店先の棚にカードを置く(下記)。
6. プレビューで確かめる(パソコン幅とスマホ幅)。

### ページの型(この順番を守る)

1. 看板:札・種別 → 商品名 → キャッチ → 紹介文 → ボタン / 右に画面写真(①②③…)
2. こんな方に / あなたが使うと、こう働きます
3. お品書き(利用条件)※ゲームなら「遊び方」でも可
4. 店主のひとこと
5. こちらの品もどうぞ(関連の品 2〜3点)
6. お問い合わせ

違うことをしたいときは、まず型どおりに作ってから、その商品だけの部分を足す。

### 札の種類

| class | 表示 | 意味 |
|---|---|---|
| `tag-stock` | 店頭在庫あり | すぐ使える |
| `tag-order` | お取り寄せ | 要相談 |
| `tag-soon` | 入荷予定 | 準備中 |
| `tag-done` | 販売終了 | 提供を終えた |

### 店先の棚に置くカード

棚の「どこに何を書くか」(カードの中身)と「どの順番で・一押しかどうか」(並び)は別の場所にあります。`index.html` の `<div class="grid">` は直接編集しません(自動生成される場所です)。

1. `goods/【フォルダ名】/card.html` を作る(実在するページが無い商品でも、このファイルだけは作る):

   ```html
   <article class="card">
     <div class="card-shot"><img src="goods/【フォルダ名】/card.png" alt="【写っているもの】" width="【幅】" height="【高さ】"></div>
     <div class="card-body">
       <div class="card-meta"><span class="tag tag-stock">店頭在庫あり</span>【種別】</div>
       <h3>【商品名】</h3>
       <p>【一行説明】</p>
       <a class="card-link" href="goods/【フォルダ名】/">詳しく見る <svg aria-hidden="true" width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 8h10M9 4l4 4-4 4"/></svg></a>
     </div>
   </article>
   ```

   画像がまだなければ、`<div class="card-shot"> … </div>` を `<div class="card-shot ph">[画面写真]</div>` にしておく。

2. `shelf-order.txt` に、そのフォルダ名を1行足す(「一押し」に入れたければその見出しの下に)。
3. `python3 tools/build_shelf.py` を実行する。`index.html` の棚が、その場で組み立て直される。

並び順を変えたい・一押しを入れ替えたいだけのときも、`shelf-order.txt` を直してから2を実行するだけでよい。

## 作業と公開の流れ

リポジトリの実体は Calypso の `~/projects/aramono_ten/`。GitHub Codespace は使わない(廃止済み)。

1. いまいるブランチが `draft` か確かめる(`git branch` で `*` が付いている方)。
2. `python3 -m http.server <割り当て済みポート>` で手元プレビュー(パソコン幅・スマホ幅の両方)。
3. 差分を見てから `git commit`。
4. `git push github draft` — まだ公開されない。
5. GitHub で `draft` → `main` のプルリクエストを開く(なければ新規作成)。差分を最後に確認してからマージ。**ここで初めて公開される**(1〜2分でPagesに反映)。
6. 本番URL(https://k1sasaki.github.io/ )で確かめる。
7. 問題なければ `git push nas --all` — NAS(`/mnt/repos/aramono_ten.git`)にも記録。nasは非公開なので、ここは気軽に。

ちまちま公開しない。ローカルでちゃんと確かめてから、まとめて一気に出す。
