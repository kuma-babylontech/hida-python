import copy
import pickle
import sys

import pytest


def test_build_cli_prefixes_every_import_with_lazy(lazy_mod):
    src = lazy_mod.build_cli(lazy=True)
    imports = [line for line in src.splitlines() if "import " in line and "sys" not in line]
    assert len(imports) == len(lazy_mod.HEAVY_MODULES)
    assert all(line.startswith("lazy import ") for line in imports)


def test_lazy_cli_loads_fewer_modules(lazy_mod, tmp_path):
    eager = tmp_path / "eager.py"
    lazy = tmp_path / "lazy.py"
    eager.write_text(lazy_mod.build_cli(lazy=False), encoding="utf-8")
    lazy.write_text(lazy_mod.build_cli(lazy=True), encoding="utf-8")
    assert lazy_mod.count_loaded(lazy) < lazy_mod.count_loaded(eager)


def test_frozen_config_is_deeply_immutable(frozendict_mod):
    config = frozendict_mod.load_frozen_config(frozendict_mod.CONFIG_JSON)
    assert isinstance(config["db"], frozendict)
    assert config["features"] == ("search", "export")
    with pytest.raises(TypeError):
        config["db"]["port"] = 3306
    hash(config)  # 中まで不変なのでハッシュできる


def test_connection_string_is_cached(frozendict_mod):
    db = frozendict(host="h", port=1)
    frozendict_mod.connection_string.cache_clear()
    frozendict_mod.connection_string(db)
    frozendict_mod.connection_string(frozendict(port=1, host="h"))
    assert frozendict_mod.connection_string.cache_info().hits == 1


def test_update_profile_distinguishes_omitted_from_none(sentinel_mod):
    user = sentinel_mod.User("a", "nick")
    sentinel_mod.update_profile(user, name="b")
    assert user.nickname == "nick"  # 渡さなければ変えない
    sentinel_mod.update_profile(user, nickname=None)
    assert user.nickname is None  # None を渡せば消す
    assert user.name == "b"


def test_sentinel_survives_copy_and_pickle(sentinel_mod):
    m = sentinel_mod.KEEP
    assert repr(m) == "KEEP"
    assert copy.deepcopy(m) is m
    assert pickle.loads(pickle.dumps(m)) is m


def test_comprehension_unpacking(small_mod):
    assert small_mod.flatten([[1, 2], [], [3]]) == [1, 2, 3]
    assert small_mod.merge_all([{"a": 1}, {"b": 2}, {"a": 3}]) == {"a": 3, "b": 2}


def test_count_primes(free_threading_mod):
    assert free_threading_mod.count_primes(30) == 10  # 2,3,5,7,11,13,17,19,23,29


def test_utf8_mode_is_default():
    assert sys.flags.utf8_mode


def test_feature_snippets_run_on_current_python(compare_mod):
    # このテストは 3.15 で走らせる前提。全機能の検証コードが通ることを確認する
    for added, name, code in compare_mod.FEATURES:
        assert compare_mod.supports(sys.executable, code), name
