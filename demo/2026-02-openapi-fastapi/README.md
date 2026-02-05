# OpenAPI × FastAPI 入門 デモ

飛騨高山Pythonの会 2026年2月のスライド連動デモアプリケーションです。

## 起動手順

```bash
docker compose up --build
```

## アクセスURL

| URL | 内容 |
|-----|------|
| http://localhost:8001/docs | Swagger UI（APIを試せる画面） |
| http://localhost:8001/redoc | ReDoc（リファレンス形式のドキュメント） |

## エンドポイント一覧

### GET /

Hello World。FastAPIの最小構成の例。

```bash
curl http://localhost:8001/
```

```json
{"message": "Hello, World!"}
```

### GET /items/{item_id}

型ヒント・パスパラメータ・クエリパラメータのデモ。

```bash
# 基本
curl http://localhost:8001/items/1

# クエリパラメータ付き
curl "http://localhost:8001/items/1?q=test"

# item_id に文字列を渡すと 422 エラー
curl http://localhost:8001/items/abc
```

### POST /items/

Pydantic モデルによるリクエストボディのデモ。

```bash
# 正常リクエスト
curl -X POST http://localhost:8001/items/ \
  -H "Content-Type: application/json" \
  -d '{"name": "りんご", "price": 150}'

# is_offer はオプション
curl -X POST http://localhost:8001/items/ \
  -H "Content-Type: application/json" \
  -d '{"name": "みかん", "price": 100, "is_offer": true}'

# price に文字列を渡すと 422 エラー
curl -X POST http://localhost:8001/items/ \
  -H "Content-Type: application/json" \
  -d '{"name": "バナナ", "price": "高い"}'
```

### GET /users/{user_id}

レスポンスモデルのデモ。返り値の型がドキュメントに反映される。

```bash
curl http://localhost:8001/users/1
```

```json
{"id": 1, "name": "田中太郎", "email": "tanaka@example.com"}
```

## 対応スライド

| エンドポイント | スライド |
|--------------|---------|
| `GET /` | FastAPIとは |
| `GET /items/{item_id}` | 型ヒントの力 |
| `POST /items/` | Pydanticモデル |
| `GET /users/{user_id}` | レスポンスモデルの定義 |
