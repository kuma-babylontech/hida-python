"""バージョン比較用の純 Python ベンチマーク（3.11 でも動く書き方に限定）。

引数なしで全ワークロードを実行し、各所要時間（秒）を JSON で出力する。
06_compare_versions.py から各バージョンのインタプリタで呼ばれる。
"""

import json
import time


def nbody(steps: int = 240_000) -> float:
    """浮動小数点演算中心（3体の重力シミュレーション）。"""
    bodies = [
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 39.47],
        [4.84, -1.16, -0.10, 0.60, 2.81, -0.02, 0.037],
        [8.34, 4.12, -0.40, -1.01, 1.82, 0.008, 0.011],
    ]
    dt = 0.01
    for _ in range(steps):
        for i in range(3):
            bi = bodies[i]
            for j in range(i + 1, 3):
                bj = bodies[j]
                dx, dy, dz = bi[0] - bj[0], bi[1] - bj[1], bi[2] - bj[2]
                mag = dt / ((dx * dx + dy * dy + dz * dz) ** 1.5)
                bi[3] -= dx * bj[6] * mag
                bi[4] -= dy * bj[6] * mag
                bi[5] -= dz * bj[6] * mag
                bj[3] += dx * bi[6] * mag
                bj[4] += dy * bi[6] * mag
                bj[5] += dz * bi[6] * mag
        for b in bodies:
            b[0] += dt * b[3]
            b[1] += dt * b[4]
            b[2] += dt * b[5]
    return bodies[0][0]


def primes(limit: int = 400_000) -> int:
    """整数演算とループ（素朴な素数判定）。"""
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


class Point:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def moved(self, dx: int) -> "Point":
        return Point(self.x + dx, self.y)


def objects(n: int = 2_400_000) -> int:
    """オブジェクト生成・属性アクセス・メソッド呼び出し。"""
    p = Point(0, 0)
    total = 0
    for i in range(n):
        p = p.moved(i % 3)
        total += p.x
    return total


def strings(n: int = 800_000) -> int:
    """文字列処理と dict 操作。"""
    counts: dict = {}
    for i in range(n):
        key = f"user-{i % 1000}".upper().replace("-", "_")
        counts[key] = counts.get(key, 0) + len(key)
    return len(counts)


WORKLOADS = {"nbody": nbody, "primes": primes, "objects": objects, "strings": strings}


def main() -> None:
    result = {}
    for name, fn in WORKLOADS.items():
        start = time.perf_counter()
        fn()
        result[name] = time.perf_counter() - start
    print(json.dumps(result))


if __name__ == "__main__":
    main()
