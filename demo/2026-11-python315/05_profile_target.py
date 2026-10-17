"""PEP 799: Tachyon（サンプリングプロファイラ）で覗くための、わざと遅い処理。

コードは一切変えずに、外からプロファイルする:

    python3.15 -m profiling.sampling run --flamegraph -o output/flame.html 05_profile_target.py
    python3.15 -m profiling.sampling run --live 05_profile_target.py      # top 風の TUI
    python3.15 -m profiling.sampling run 05_profile_target.py             # 表で出す
"""

import json
import re

WORD = re.compile(r"[a-z]+")


def make_documents(n: int) -> list[str]:
    return [json.dumps({"id": i, "body": "python hida takayama " * (i % 50)}) for i in range(n)]


def slow_word_count(docs: list[str]) -> dict[str, int]:
    """毎回 json.loads して正規表現で数える（ここがホットスポットになるはず）。"""
    counts: dict[str, int] = {}
    for doc in docs:
        body = json.loads(doc)["body"]
        for word in WORD.findall(body):
            counts[word] = counts.get(word, 0) + 1
    return counts


def slow_primes(limit: int) -> int:
    """素朴な素数判定（CPU を食うもう一つの山）。"""
    return sum(1 for n in range(2, limit) if all(n % d for d in range(2, int(n**0.5) + 1)))


def main() -> None:
    docs = make_documents(60_000)
    print(slow_word_count(docs))
    print(slow_primes(200_000))


if __name__ == "__main__":
    main()
