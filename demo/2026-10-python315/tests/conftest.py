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
def lazy_mod():
    return _load("lazy_imports", "01_lazy_imports.py")


@pytest.fixture(scope="session")
def frozendict_mod():
    return _load("frozendict_demo", "02_frozendict.py")


@pytest.fixture(scope="session")
def sentinel_mod():
    return _load("sentinel_demo", "03_sentinel.py")


@pytest.fixture(scope="session")
def small_mod():
    return _load("small_changes", "04_small_changes.py")


@pytest.fixture(scope="session")
def free_threading_mod():
    return _load("free_threading", "07_free_threading.py")


@pytest.fixture(scope="session")
def compare_mod():
    return _load("compare_versions", "06_compare_versions.py")
