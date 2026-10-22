#!/usr/bin/env python3
"""includer.py → build_shelf.py → build_related.py を順番に実行する。

何を変えたときにどれを流せばいいか覚えなくて済むように、まとめて全部流す。
変更が無いものは「変更なし。」と言うだけなので、流しすぎても害はない。

使い方(リポジトリのルートで):
  python3 tools/build_all.py
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

STEPS = [
    [sys.executable, "tools/includer.py", "--parts", "parts", "--target", "."],
    [sys.executable, "tools/build_shelf.py"],
    [sys.executable, "tools/build_related.py"],
]


def main():
    for cmd in STEPS:
        print(f"$ {' '.join(cmd)}")
        result = subprocess.run(cmd, cwd=ROOT)
        if result.returncode != 0:
            print(f"エラー: {cmd[1]} が失敗しました。ここで止めます。", file=sys.stderr)
            sys.exit(result.returncode)


if __name__ == "__main__":
    main()
