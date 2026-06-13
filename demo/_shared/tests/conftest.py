"""
reinfolib は数字始まりでない通常モジュールなので、
テストからは _shared ディレクトリを import パスに足して読み込む。
"""

import sys
from pathlib import Path

SHARED_DIR = Path(__file__).resolve().parent.parent
if str(SHARED_DIR) not in sys.path:
    sys.path.insert(0, str(SHARED_DIR))
