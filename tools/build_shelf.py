#!/usr/bin/env python3
"""トップページの棚(品揃え)を組み立てるツール。

shelf-order.txt に書かれた順番で、各 goods/<名前>/card.html を集めて、
index.html の <!-- include:shelf --> ... <!-- /include:shelf --> のあいだに
書き込む(増殖はしない。常に置き換え)。

shelf-order.txt は「# 一押し」「# それ以外」の見出しで2つのグループに分け、
その下に goods/ のフォルダ名を1行ずつ書く。「一押し」に1つでも名前があれば、
見出し付きの小さい棚として先頭に出す。

使い方:
  python3 tools/build_shelf.py --order shelf-order.txt --goods goods --target index.html

商品を足すときは:
  1. goods/<名前>/card.html に、そのカードの中身(<article class="card">…</article>)を書く
  2. shelf-order.txt に <名前> を1行足す
  3. このスクリプトを実行する
"""
import argparse
import re
import sys
from pathlib import Path

KNOWN_GROUPS = ("一押し", "それ以外")


def parse_order_file(path: Path):
    groups = {name: [] for name in KNOWN_GROUPS}
    current = None
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if line.startswith("#"):
            label = line.lstrip("#").strip()
            if label not in groups:
                print(f"エラー: 不明な見出しです: {raw_line}", file=sys.stderr)
                sys.exit(1)
            current = label
            continue
        if current is None:
            print(f"エラー: 見出しより先に商品名が書かれています: {raw_line}", file=sys.stderr)
            sys.exit(1)
        groups[current].append(line)
    return groups


def find_span(content: str, name: str):
    start_re = re.compile(r"<!--\s*include:%s\s*-->" % re.escape(name))
    end_re = re.compile(r"<!--\s*/include:%s\s*-->" % re.escape(name))
    starts = list(start_re.finditer(content))
    ends = list(end_re.finditer(content))
    if len(starts) != 1 or len(ends) != 1:
        print(
            f"エラー: 目印 'include:{name}' の開始{len(starts)}個・終了{len(ends)}個。"
            f" ちょうど1組のはずなので、書き込みません。",
            file=sys.stderr,
        )
        sys.exit(1)
    s, e = starts[0], ends[0]
    if s.end() > e.start():
        print(f"エラー: 目印 'include:{name}' の開始と終了の順番がおかしいです。", file=sys.stderr)
        sys.exit(1)
    return s, e


def indent(text: str, prefix: str) -> str:
    return "\n".join(prefix + line if line else line for line in text.split("\n"))


def render_group(goods_dir: Path, names: list[str]) -> list[str]:
    cards = []
    for name in names:
        card_path = goods_dir / name / "card.html"
        if not card_path.exists():
            print(f"エラー: {card_path} が見つかりません", file=sys.stderr)
            sys.exit(1)
        cards.append(card_path.read_text(encoding="utf-8").rstrip("\n"))
    return cards


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--order", default="shelf-order.txt")
    ap.add_argument("--goods", default="goods")
    ap.add_argument("--target", default="index.html")
    args = ap.parse_args()

    groups = parse_order_file(Path(args.order))
    goods_dir = Path(args.goods)
    target_path = Path(args.target)

    featured = render_group(goods_dir, groups["一押し"])
    regular = render_group(goods_dir, groups["それ以外"])

    base = "      "  # <div class="shelf-head"> と同じ深さ
    card_indent = base + "  "

    parts = []
    if featured:
        parts.append(base + '<h3 class="sub">一押し</h3>')
        parts.append(base + '<div class="grid">')
        parts.append("")
        parts.append(("\n\n").join(indent(c, card_indent) for c in featured))
        parts.append("")
        parts.append(base + "</div>")
        parts.append("")
    parts.append(base + '<div class="grid">')
    parts.append("")
    parts.append(("\n\n").join(indent(c, card_indent) for c in regular))
    parts.append("")
    parts.append(base + "</div>")

    shelf_html = "\n".join(parts)

    content = target_path.read_text(encoding="utf-8")
    s, e = find_span(content, "shelf")
    new_content = content[: s.end()] + "\n" + shelf_html + "\n" + base + content[e.start() :]

    if new_content == content:
        print("変更なし。")
    else:
        target_path.write_text(new_content, encoding="utf-8")
        print(f"更新: {target_path}")


if __name__ == "__main__":
    main()
