#!/usr/bin/env python3
"""各商品ページの「こちらの品もどうぞ」を自動生成するツール。

shelf-order.txt に載っている他の商品の中から、商品名をシードにした
決め打ちランダムで --count 件選び、その商品の goods/<名前>/card.html に
あるタイトル・説明文・リンク先をそのまま使って
goods/<自分>/index.html の <!-- include:related --> ... <!-- /include:related -->
のあいだを書き換える(増殖はしない。常に置き換え)。

同じ shelf-order.txt・同じ商品名である限り、何度実行しても同じ組み合わせになる
(商品が増えたときだけ選ばれ方が変わる)。

使い方:
  python3 tools/build_related.py --order shelf-order.txt --goods goods --count 2

index.html側の <!-- include:related --> の外側は <!-- #region --> + div で
囲ってあるので、直接いじってしまう事故を減らせる(shelf/headerと同じ仕組み)。
"""
import argparse
import random
import re
import sys
from pathlib import Path


def flat_order(path: Path) -> list[str]:
    names = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        names.append(line)
    return names


def parse_card(goods_dir: Path, name: str):
    card_path = goods_dir / name / "card.html"
    if not card_path.exists():
        print(f"エラー: {card_path} が見つかりません", file=sys.stderr)
        sys.exit(1)
    text = card_path.read_text(encoding="utf-8")
    title_m = re.search(r"<h3>(.*?)</h3>", text, re.S)
    desc_m = re.search(r"<p>(.*?)</p>", text, re.S)
    href_m = re.search(r'<a class="card-link" href="([^"]+)"', text)
    if not (title_m and desc_m and href_m):
        print(f"エラー: {card_path} からタイトル・説明・リンクを読み取れません", file=sys.stderr)
        sys.exit(1)
    return title_m.group(1).strip(), desc_m.group(1).strip(), href_m.group(1).strip()


def convert_href(href: str) -> str:
    if href.startswith("goods/"):
        return "../" + href[len("goods/") :]
    return href  # http(s):// や #contact はそのまま


def render_related(goods_dir: Path, names: list[str]) -> str:
    lines = [
        '<section class="wrap section" style="display: flex; flex-direction: column; gap: 20px;">',
        '  <h2 class="sub">こちらの品もどうぞ</h2>',
        '  <div class="links">',
    ]
    for name in names:
        title, desc, href = parse_card(goods_dir, name)
        href = convert_href(href)
        lines.append(f'    <a class="link-card" href="{href}">')
        lines.append(f"      <strong>{title}</strong>")
        lines.append(f"      <span>{desc}</span>")
        lines.append("    </a>")
    lines.append("  </div>")
    lines.append("</section>")
    return "\n".join(lines)


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


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--order", default="shelf-order.txt")
    ap.add_argument("--goods", default="goods")
    ap.add_argument("--count", type=int, default=2)
    args = ap.parse_args()

    goods_dir = Path(args.goods)
    all_names = flat_order(Path(args.order))

    changed = []
    for name in all_names:
        target_path = goods_dir / name / "index.html"
        if not target_path.exists():
            continue  # このページはまだ無い(商品はあるがサイト内ページ未作成)

        others = [n for n in all_names if n != name]
        k = min(args.count, len(others))
        picks = random.Random(name).sample(others, k)

        related_html = indent(render_related(goods_dir, picks), "  ")

        content = target_path.read_text(encoding="utf-8")
        s, e = find_span(content, "related")
        new_content = content[: s.end()] + "\n" + related_html + "\n" + "  " + content[e.start() :]

        if new_content != content:
            target_path.write_text(new_content, encoding="utf-8")
            changed.append(str(target_path))

    if changed:
        print("更新:")
        for c in changed:
            print(f"  {c}")
    else:
        print("変更なし。")


if __name__ == "__main__":
    main()
