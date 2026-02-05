"""OpenAPI × FastAPI 入門 - デモアプリケーション

飛騨高山Pythonの会 2026年2月 スライド連動デモ
"""

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(
    title="OpenAPI × FastAPI 入門 デモAPI",
    description="飛騨高山Pythonの会 2026年2月のスライド連動デモアプリケーションです。",
    version="1.0.0",
)


# ------------------------------------
# 1. Hello World（スライド「FastAPIとは」）
# ------------------------------------
@app.get("/")
def read_root():
    return {"message": "Hello, World!"}


# ------------------------------------
# 2. 型ヒント・パスパラメータ・クエリパラメータ（スライド「型ヒントの力」）
# ------------------------------------
@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}


# ------------------------------------
# 3. Pydantic モデルによるリクエストボディ（スライド「Pydanticモデル」）
# ------------------------------------
class Item(BaseModel):
    name: str
    price: float
    is_offer: bool | None = None


@app.post("/items/")
def create_item(item: Item):
    return {"item_name": item.name, "item_price": item.price}


# ------------------------------------
# 4. レスポンスモデル（スライド「レスポンスモデルの定義」）
# ------------------------------------
class UserResponse(BaseModel):
    id: int
    name: str
    email: str


@app.get("/users/{user_id}")
def get_user(user_id: int) -> UserResponse:
    return UserResponse(
        id=user_id,
        name="田中太郎",
        email="tanaka@example.com",
    )
