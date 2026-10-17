"""PEP 810: lazy import で CLI の起動時間がどう変わるかを測る。

重い標準ライブラリを import するだけの「--help しか使わない CLI」を
通常 import 版と lazy import 版の2つ生成し、それぞれ別プロセスで起動して比べる。

    python3.15 01_lazy_imports.py
"""

import statistics
import subprocess
import sys
import tempfile
import time
from pathlib import Path

# 起動時に import されるが、--help だけなら一度も使われないモジュール群
HEAVY_MODULES = [
    "asyncio",
    "decimal",
    "email.mime.multipart",
    "http.client",
    "json",
    "sqlite3",
    "xml.etree.ElementTree",
    "zipfile",
]

HELP_BODY = """
import sys
if "--help" in sys.argv:
    print("usage: mytool [--help] <command>")
    sys.exit(0)
"""


def build_cli(*, lazy: bool, imports: bool = True) -> str:
    """HEAVY_MODULES を import してから --help を処理する CLI のソースを返す。"""
    if not imports:
        return HELP_BODY
    prefix = "lazy " if lazy else ""
    return "\n".join(f"{prefix}import {m}" for m in HEAVY_MODULES) + "\n" + HELP_BODY


def measure(script: Path, runs: int = 20) -> float:
    """script を --help 付きで runs 回起動し、所要時間の中央値（ミリ秒）を返す。"""
    times = []
    for _ in range(runs):
        start = time.perf_counter()
        subprocess.run([sys.executable, str(script), "--help"], check=True, capture_output=True)
        times.append((time.perf_counter() - start) * 1000)
    return statistics.median(times)


def count_loaded(script: Path) -> int:
    """script を（--help なしで）実行した直後の sys.modules の件数を返す。"""
    probe = f"import runpy, sys; runpy.run_path({str(script)!r}); print(len(sys.modules))"
    out = subprocess.run([sys.executable, "-c", probe], check=True, capture_output=True, text=True)
    return int(out.stdout.strip().splitlines()[-1])


def main() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        scripts = {}
        for name, kwargs in {
            "empty": {"lazy": False, "imports": False},
            "eager": {"lazy": False},
            "lazy": {"lazy": True},
        }.items():
            path = Path(tmp) / f"{name}_cli.py"
            path.write_text(build_cli(**kwargs), encoding="utf-8")
            scripts[name] = path

        t = {name: measure(path) for name, path in scripts.items()}
        print(f"Python {sys.version.split()[0]} / --help の起動時間（中央値・20回）")
        print(f"  import なし   : {t['empty']:6.1f} ms")
        print(f"  通常の import : {t['eager']:6.1f} ms")
        print(f"  lazy import   : {t['lazy']:6.1f} ms")
        print(f"  → import 部分 {t['eager'] - t['empty']:.1f} ms が {t['lazy'] - t['empty']:.1f} ms に")
        print(
            f"  読み込まれたモジュール数: 通常 {count_loaded(scripts['eager'])}"
            f" / lazy {count_loaded(scripts['lazy'])}"
        )


if __name__ == "__main__":
    main()
