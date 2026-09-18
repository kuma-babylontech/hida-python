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
def common_mod():
    return _load("common", "common.py")


@pytest.fixture(scope="session")
def without_rag_mod():
    return _load("ask_without_rag", "01_ask_without_rag.py")


@pytest.fixture(scope="session")
def kb_retrieve_mod():
    return _load("kb_retrieve", "02_kb_retrieve.py")


@pytest.fixture(scope="session")
def kb_rag_mod():
    return _load("kb_retrieve_and_generate", "03_kb_retrieve_and_generate.py")


@pytest.fixture(scope="session")
def diy_rag_mod():
    return _load("diy_rag", "04_diy_rag.py")
