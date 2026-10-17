"""PEP 661: sentinel で「引数が渡されなかった」と「None が渡された」を区別する。

例: プロフィールの更新。ニックネームを
  - 渡さなければ「変えない」
  - None を渡せば「消す」
  - 文字列を渡せば「書き換える」

    python3.15 03_sentinel.py
"""

import copy
import pickle
from dataclasses import dataclass

KEEP = sentinel("KEEP")


@dataclass
class User:
    name: str
    nickname: str | None = None


def update_profile(user: User, name: str | KEEP = KEEP, nickname: str | None | KEEP = KEEP) -> None:
    """渡された項目だけを書き換える。"""
    if name is not KEEP:
        user.name = name
    if nickname is not KEEP:
        user.nickname = nickname  # None なら「ニックネームなし」にする


def main() -> None:
    user = User("飛騨太郎", "ひだ")

    update_profile(user, name="飛騨次郎")
    print("名前だけ変更        →", user)  # ニックネームは「ひだ」のまま

    update_profile(user, nickname=None)
    print("ニックネームを消す  →", user)

    # 以前の定番 `KEEP = object()` との違い
    old = object()
    print()
    print("repr  : object() →", repr(old), "/ sentinel →", repr(KEEP))
    print("copy  : 同一性を保つ?", copy.deepcopy(KEEP) is KEEP)
    print("pickle: 同一性を保つ?", pickle.loads(pickle.dumps(KEEP)) is KEEP)  # 自分で作ったデータのみ


if __name__ == "__main__":
    main()
