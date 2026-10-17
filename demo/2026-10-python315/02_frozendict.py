"""PEP 814: frozendict（変更できない・ハッシュできる dict）を使ってみる。

    python3.15 02_frozendict.py
"""

import functools
import json

CONFIG_JSON = '{"db": {"host": "localhost", "port": 5432}, "features": ["search", "export"]}'


def load_frozen_config(text: str) -> frozendict:
    """JSON を「中まで丸ごと変更不可」な frozendict / tuple に変換して読む。

    3.15 で json に array_hook が入ったので、object_hook と組み合わせれば一発。
    """
    return json.loads(text, object_hook=frozendict, array_hook=tuple)


@functools.cache
def connection_string(db: frozendict) -> str:
    """dict は unhashable なので @cache の引数にできないが、frozendict なら渡せる。"""
    print("  （計算しました）")
    return f"postgresql://{db['host']}:{db['port']}"


def main() -> None:
    config = load_frozen_config(CONFIG_JSON)
    print("読み込んだ設定:", config)

    try:
        config["db"]["port"] = 3306
    except TypeError as e:
        print("書き換えようとすると →", e)

    print("1回目:", connection_string(config["db"]))
    print("2回目:", connection_string(config["db"]))  # キャッシュが効く

    # 順序が違っても中身が同じなら等しく、ハッシュも同じ
    a = frozendict(x=1, y=2)
    b = frozendict(y=2, x=1)
    print("a == b:", a == b, "/ hash 一致:", hash(a) == hash(b))
    print("dict のサブクラス?:", isinstance(a, dict))  # False。Mapping として扱う
    print("dict との合成:", a | {"z": 3})


if __name__ == "__main__":
    main()
