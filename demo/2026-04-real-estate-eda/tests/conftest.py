"""
デモスクリプトは `01_fetch_data.py` のように数字始まりで `import` できないので、
`importlib.util` で動的ロードしてフィクスチャとして提供する。
"""

import importlib.util
import sys
from pathlib import Path

import pytest

DEMO_DIR = Path(__file__).resolve().parent.parent


def _load(module_name: str, filename: str):
    spec = importlib.util.spec_from_file_location(module_name, DEMO_DIR / filename)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="session")
def fetch_data_mod():
    return _load("fetch_data", "01_fetch_data.py")


@pytest.fixture(scope="session")
def descriptive_mod():
    return _load("descriptive_stats", "02_descriptive_stats.py")
