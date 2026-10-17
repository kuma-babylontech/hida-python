"""3.15 の「小さいけど日々効く」変更をまとめて実行する。

    python3.15 04_small_changes.py
"""

import locale
import re
import sys
import traceback
from collections import Counter
from typing import TypedDict


def flatten(rows: list[list[int]]) -> list[int]:
    """PEP 798: 内包表記の中で * アンパックができる。"""
    return [*row for row in rows]  # 以前は [x for row in rows for x in row]


def merge_all(dicts: list[dict]) -> dict:
    """PEP 798: dict 内包表記でも ** が使える（後勝ち）。"""
    return {**d for d in dicts}


class Movie(TypedDict, closed=True):
    """PEP 728: closed=True で「宣言していないキー」を型チェッカーが弾く。"""

    title: str
    year: int


def section(title: str) -> None:
    print(f"\n== {title}")


def main() -> None:
    section("内包表記のアンパック（PEP 798）")
    print(flatten([[1, 2], [3], [4, 5]]))
    print(merge_all([{"a": 1}, {"b": 2}, {"a": 3}]))

    section("UTF-8 がデフォルトに（PEP 686）")
    print("UTF-8 モード:", bool(sys.flags.utf8_mode))
    print("open() の既定エンコーディング:", locale.getpreferredencoding(False))

    section("他言語のクセに寄り添うエラーメッセージ")
    for code in ["[].push(1)", "'a'.toUpperCase()", "{}.put('k', 1)", "(1, 2).append(3)"]:
        try:
            exec(code)  # デモ用の固定文字列のみを実行する
        except AttributeError as e:
            print(f"{code:20} → {traceback.format_exception_only(e)[-1].strip()}")

    section("re.prefixmatch()（re.match の分かりやすい別名）")
    print(re.prefixmatch(r"\d+", "2026年"))

    section("Counter の対称差 ^")
    print(Counter(python=3, rust=1) ^ Counter(python=1, go=2))

    section("TypedDict(closed=True)（PEP 728）")
    print("Movie.__closed__ =", Movie.__closed__)


if __name__ == "__main__":
    main()
