"""3.10〜3.15 を並べて「使える機能」と「速さ」を比べる。

各バージョンのインタプリタは `uv python find 3.X` で探す（無ければ `uv python install 3.10 3.11 3.12 3.13 3.14 3.15`）。
結果は標準出力と output/compare.md に書き出す。

    python3.15 06_compare_versions.py            # 機能表 + ベンチマーク
    python3.15 06_compare_versions.py --features # 機能表だけ
"""

import json
import os
import platform
import statistics
import subprocess
import sys
from pathlib import Path

VERSIONS = ["3.10", "3.11", "3.12", "3.13", "3.14", "3.15"]
HERE = Path(__file__).parent
OUTPUT = HERE / "output"

# (追加されたバージョン, 機能名, そのバージョンで動けば成功するコード)
FEATURES = [
    ("3.11", "except* / ExceptionGroup", "try:\n    raise ExceptionGroup('g', [ValueError()])\nexcept* ValueError:\n    pass"),
    ("3.11", "tomllib", "import tomllib; tomllib.loads('a = 1')"),
    ("3.12", "type 文・ジェネリクス構文", "type Pair[T] = tuple[T, T]\ndef first[T](p: Pair[T]) -> T: return p[0]"),
    ("3.12", "f-string 内で同じ引用符", "d = {'k': 1}; f'{d['k']}'"),
    ("3.13", "copy.replace()", "import copy, dataclasses\n@dataclasses.dataclass\nclass P: x: int\ncopy.replace(P(1), x=2)"),
    ("3.13", "warnings.deprecated", "from warnings import deprecated"),
    ("3.14", "t-string", "t'hello {1 + 1}'"),
    ("3.14", "括弧なし except A, B", "try:\n    pass\nexcept ValueError, TypeError:\n    pass"),
    ("3.14", "compression.zstd", "from compression import zstd"),
    ("3.15", "lazy import", "lazy import json"),
    ("3.15", "frozendict", "hash(frozendict(a=1))"),
    ("3.15", "sentinel", "MISSING = sentinel('MISSING')"),
    ("3.15", "内包表記の * アンパック", "[*xs for xs in [[1], [2]]]"),
    ("3.15", "UTF-8 がデフォルト", "import sys; assert sys.flags.utf8_mode"),
]


def find_python(version: str) -> str | None:
    # Homebrew 等とビルド条件が混ざると速度比較が歪むので、uv 管理のビルドに揃える
    out = subprocess.run(["uv", "python", "find", "--managed-python", version], capture_output=True, text=True)
    return out.stdout.strip() or None


def supports(python: str, code: str) -> bool:
    """code をモジュールとして実行し、構文エラー・例外なく終われば True。"""
    env = {k: v for k, v in os.environ.items() if k != "PYTHONUTF8"}
    return subprocess.run([python, "-c", code], capture_output=True, env=env).returncode == 0


def feature_table(pythons: dict[str, str]) -> str:
    header = "| 機能 | 追加 | " + " | ".join(pythons) + " |"
    lines = [header, "|" + "---|" * (len(pythons) + 2)]
    for added, name, code in FEATURES:
        marks = ["✅" if supports(py, code) else "—" for py in pythons.values()]
        lines.append(f"| {name} | {added} | " + " | ".join(marks) + " |")
    return "\n".join(lines)


def bench(python: str, runs: int, jit: bool = False) -> dict[str, float]:
    """bench_workload.py を runs 回実行し、ワークロードごとの中央値（秒）を返す。"""
    env = dict(os.environ, PYTHON_JIT="1" if jit else "0")
    samples: dict[str, list[float]] = {}
    for _ in range(runs):
        out = subprocess.run(
            [python, str(HERE / "bench_workload.py")], capture_output=True, text=True, env=env, check=True
        )
        for name, sec in json.loads(out.stdout).items():
            samples.setdefault(name, []).append(sec)
    return {name: statistics.median(v) for name, v in samples.items()}


def bench_table(pythons: dict[str, str], runs: int) -> str:
    rows = {f"{v}": bench(py, runs) for v, py in pythons.items()}
    if "3.15" in pythons:
        rows["3.15 + JIT"] = bench(pythons["3.15"], runs, jit=True)
    base = rows[next(iter(rows))]
    names = list(base)
    lines = [
        "| バージョン | " + " | ".join(names) + " | 合計 | 3.10 比 |",
        "|" + "---|" * (len(names) + 3),
    ]
    base_total = sum(base.values())
    for label, r in rows.items():
        total = sum(r.values())
        cells = " | ".join(f"{r[n]:.3f}" for n in names)
        lines.append(f"| {label} | {cells} | {total:.3f} | {base_total / total:.2f}x |")
    return "\n".join(lines)


def main() -> None:
    pythons = {v: p for v in VERSIONS if (p := find_python(v))}
    missing = [v for v in VERSIONS if v not in pythons]
    if missing:
        print("見つからないバージョン:", ", ".join(missing), "（uv python install で追加できます）")

    sections = [f"環境: {platform.system()} {platform.machine()}"]
    for v, p in pythons.items():
        ver = subprocess.run([p, "-c", "import sys; print(sys.version.split()[0])"], capture_output=True, text=True)
        sections[0] += f" / {ver.stdout.strip()}"

    sections.append("## 使える機能\n\n" + feature_table(pythons))
    if "--features" not in sys.argv:
        runs = 5
        sections.append(f"## 実行時間（秒・{runs}回の中央値、小さいほど速い）\n\n" + bench_table(pythons, runs))

    report = "\n\n".join(sections)
    print(report)
    OUTPUT.mkdir(exist_ok=True)
    (OUTPUT / "compare.md").write_text(report + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
