#!/usr/bin/env python3
"""HTMLの部品差し込みツール。

対象フォルダ内の *.html を走査し、
  <!-- include:名前 -->
  ...
  <!-- /include:名前 -->
のあいだを、部品フォルダの <名前>.html の中身で置き換える(増殖はしない。常に置き換え)。

部品の中では {{BASE}} と {{HOME}} が使える。ファイルの深さに応じて、
  深さ0(トップ)      BASE="",      HOME="./"
  深さN(N階層下)      BASE="../"*N, HOME="../"*N
に置き換わる。

使い方:
  python3 includer.py --parts parts --target .

目印が0組ならそのページでは何もしない(その部品を使っていないだけ)。
1組以外(0組の開始/終了の数が食い違う、2組以上など)はエラーにして、
そのファイルには一切書き込まない。
"""
import argparse
import re
import sys
from pathlib import Path


def compute_base_home(html_path: Path, target_root: Path) -> tuple[str, str]:
    depth = len(html_path.resolve().parent.relative_to(target_root.resolve()).parts)
    if depth == 0:
        return "", "./"
    base = "../" * depth
    return base, base


def find_span(content: str, name: str):
    start_re = re.compile(r"<!--\s*include:%s\s*-->" % re.escape(name))
    end_re = re.compile(r"<!--\s*/include:%s\s*-->" % re.escape(name))
    starts = list(start_re.finditer(content))
    ends = list(end_re.finditer(content))

    if not starts and not ends:
        return None, None  # このページはこの部品を使っていない

    if len(starts) != 1 or len(ends) != 1:
        return None, (
            f"目印 'include:{name}' の開始{len(starts)}個・終了{len(ends)}個。"
            f" ちょうど1組のはずなので、このファイルには何も書き込みません。"
        )

    s, e = starts[0], ends[0]
    if s.end() > e.start():
        return None, f"目印 'include:{name}' の開始と終了の順番がおかしいです。"

    return (s, e), None


def apply_part(content: str, name: str, part_text: str):
    span, err = find_span(content, name)
    if err:
        return content, err
    if span is None:
        return content, None
    s, e = span
    new_content = (
        content[: s.end()]
        + "\n"
        + part_text.strip("\n")
        + "\n"
        + content[e.start() :]
    )
    return new_content, None


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--parts", required=True, help="部品ファイル(<名前>.html)を集めたフォルダ")
    ap.add_argument("--target", required=True, help="このフォルダ以下の *.html すべてが対象")
    ap.add_argument("--ext", default="html")
    args = ap.parse_args()

    parts_dir = Path(args.parts)
    target_root = Path(args.target)

    parts = {}
    for p in sorted(parts_dir.glob(f"*.{args.ext}")):
        parts[p.stem] = p.read_text(encoding="utf-8")

    if not parts:
        print(f"部品が見つかりません: {parts_dir}", file=sys.stderr)
        sys.exit(1)

    changed = []
    errors = []

    for html_file in sorted(target_root.rglob(f"*.{args.ext}")):
        if parts_dir.resolve() in html_file.resolve().parents:
            continue
        original = html_file.read_text(encoding="utf-8")
        content = original
        base, home = compute_base_home(html_file, target_root)
        for name, raw in parts.items():
            text = raw.replace("{{BASE}}", base).replace("{{HOME}}", home)
            content, err = apply_part(content, name, text)
            if err:
                errors.append(f"{html_file}: {err}")
        if content != original:
            html_file.write_text(content, encoding="utf-8")
            changed.append(str(html_file))

    for c in changed:
        print(f"更新: {c}")
    if not changed:
        print("変更なし。")
    for e in errors:
        print(f"エラー: {e}", file=sys.stderr)

    if errors:
        sys.exit(1)


if __name__ == "__main__":
    main()
