"""PEP 661: sentinel で「引数が渡されなかった」と「None が渡された」を区別する。

    python3.15 03_sentinel.py
"""

import copy
import pickle

MISSING = sentinel("MISSING")

_store = {"name": "飛騨高山", "nickname": None}


def get(key: str, default=MISSING) -> object:
    """default を省略したときだけ KeyError にする（None を既定値として渡すことはできる）。"""
    if key in _store:
        return _store[key]
    if default is MISSING:
        raise KeyError(key)
    return default


def main() -> None:
    print("get('nickname')           →", get("nickname"))
    print("get('age', None)          →", get("age", None))
    try:
        get("age")
    except KeyError as e:
        print("get('age')                → KeyError", e)

    # 以前の定番 `MISSING = object()` との違い
    old = object()
    print()
    print("repr  : object() →", repr(old), "/ sentinel →", repr(MISSING))
    print("copy  : 同一性を保つ?", copy.deepcopy(MISSING) is MISSING)
    print("pickle: 同一性を保つ?", pickle.loads(pickle.dumps(MISSING)) is MISSING)


if __name__ == "__main__":
    main()
