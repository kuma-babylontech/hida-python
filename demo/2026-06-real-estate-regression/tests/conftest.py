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
def simple_reg_mod():
    return _load("simple_regression", "01_simple_regression.py")


@pytest.fixture(scope="session")
def multi_reg_mod():
    return _load("multiple_regression", "02_multiple_regression.py")


@pytest.fixture(scope="session")
def underpriced_mod():
    return _load("find_underpriced", "03_find_underpriced.py")
