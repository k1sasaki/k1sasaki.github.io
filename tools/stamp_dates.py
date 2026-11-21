#!/usr/bin/env python3
"""ページのフッターにある「最終更新 YYYY-MM-DD」を、今日の日付に書き換える。

対象は git 的に変更がある(編集済み・新規追加の)HTMLファイルだけ。
変更の無いページの日付は触らない。新規ページのテンプレート由来の
プレースホルダー「最終更新 【YYYY-MM-DD】」も、初めてコミットする
タイミングで日付が入る。

build_all.py の最後の工程として呼ばれる想定(単独でも実行可)。

使い方(リポジトリのルートで):
  python3 tools/stamp_dates.py
"""
import datetime
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PATTERN = re.compile(r"(最終更新\s*)(\d{4}-\d{2}-\d{2}|【YYYY-MM-DD】)")


def dirty_html_files():
    result = subprocess.run(
        ["git", "status", "--porcelain"], cwd=ROOT, capture_output=True, text=True, check=True
    )
    files = []
    for line in result.stdout.splitlines():
        status, path = line[:2], line[3:]
        if status.strip("?") == "" and status != "??":
            continue
        if not path.endswith(".html"):
            continue
        files.append(ROOT / path)
    return files


def main():
    today = datetime.date.today().isoformat()
    changed = []
    for path in dirty_html_files():
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        new_text, n = PATTERN.subn(lambda m: m.group(1) + today, text)
        if n and new_text != text:
            path.write_text(new_text, encoding="utf-8")
            changed.append(str(path.relative_to(ROOT)))

    if changed:
        print("更新:")
        for c in changed:
            print(f"  {c}")
    else:
        print("変更なし。")


if __name__ == "__main__":
    main()
