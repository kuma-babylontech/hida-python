"""GIL あり／なしで、同じ計算を4スレッドに分けたときの速さを比べる。

    python3.15  07_free_threading.py   # 通常版（GIL あり）
    python3.15t 07_free_threading.py   # GIL なし版（free-threading）
"""

import sys
import time
from concurrent.futures import ThreadPoolExecutor

THREADS = 4
LIMIT = 400_000  # 各スレッドがこの数までの素数を数える


def count_primes(limit: int) -> int:
    count = 0
    for n in range(2, limit):
        d = 2
        while d * d <= n:
            if n % d == 0:
                break
            d += 1
        else:
            count += 1
    return count


def measure(threads: int) -> float:
    """count_primes を threads 個のスレッドで同時に走らせ、かかった秒数を返す。"""
    start = time.perf_counter()
    with ThreadPoolExecutor(max_workers=threads) as pool:
        list(pool.map(count_primes, [LIMIT] * threads))
    return time.perf_counter() - start


def gil_enabled() -> bool:
    return sys._is_gil_enabled() if hasattr(sys, "_is_gil_enabled") else True


def main() -> None:
    one = measure(1)
    many = measure(THREADS)
    label = "GIL あり" if gil_enabled() else "GIL なし"
    print(f"Python {sys.version.split()[0]}（{label}）")
    print(f"  1スレッドで1回分 : {one:.2f} 秒")
    print(f"  {THREADS}スレッドで{THREADS}回分 : {many:.2f} 秒（1回分の {many / one:.1f} 倍）")


if __name__ == "__main__":
    main()
