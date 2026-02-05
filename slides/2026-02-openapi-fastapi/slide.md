---
title: "OpenAPI × FastAPI 入門"
date: 2026-02-08
description: "APIの基礎からOpenAPI仕様、FastAPIの魅力まで。初心者向けにモダンなAPI開発スタイルをわかりやすく解説します。"
tags:
  - FastAPI
  - OpenAPI
  - 入門
---

# OpenAPI × FastAPI 入門

モダンなAPI開発のはじめかた

飛騨高山Pythonの会 2026年2月

---

## 今日のアジェンダ

1. APIってなに？
2. API開発の課題
3. OpenAPIという解決策
4. FastAPIの魅力
5. FastAPI × OpenAPI の連携
6. モダン開発スタイルとの親和性

---

## APIってなに？

**A**pplication **P**rogramming **I**nterface

ソフトウェア同士が会話するための「窓口」

```
┌──────────┐         ┌──────────┐
│  フロント  │ ─ HTTP → │  サーバー  │
│  (ブラウザ) │ ← JSON ─ │  (API)   │
└──────────┘         └──────────┘
```

身近な例: 天気予報アプリ、SNSのログイン連携、決済

---

## REST API のイメージ

HTTPメソッドで「何をしたいか」を表現

| メソッド | 意味 | 例 |
|---------|------|-----|
| GET | 取得 | ユーザー情報を取得 |
| POST | 作成 | 新しいユーザーを登録 |
| PUT | 更新 | プロフィールを変更 |
| DELETE | 削除 | アカウントを削除 |

```
GET  /api/users/123  → { "name": "田中", "age": 30 }
POST /api/users      → 新しいユーザーを作成
```

---

## API開発でよくある課題

--

### ドキュメントの問題

- 仕様書を書くのが面倒...
- コードと仕様書がズレる...
- 「このAPIの使い方がわからない」

--

### チーム開発の問題

- フロントとバックエンドの認識がズレる
- APIの仕様変更が伝わらない
- テスト環境の整備が大変

--

### コード品質の問題

- 入力値のバリデーションが漏れる
- レスポンス形式が統一されない
- エラーハンドリングがバラバラ

---

## OpenAPI とは

APIの仕様を記述するための**標準フォーマット**

- 旧称: Swagger Specification
- 最新バージョン: OpenAPI 3.2（FastAPIは3.1対応）
- YAML または JSON で記述

```yaml
openapi: 3.1.0
info:
  title: ユーザーAPI
  version: 1.0.0
paths:
  /users/{id}:
    get:
      summary: ユーザー情報を取得
```

---

## OpenAPI でできること

- **Swagger UI** - ブラウザでAPIを試せる
- **自動ドキュメント生成** - 常に最新の仕様書
- **クライアントコード自動生成** - TypeScript, Python, etc.
- **バリデーション** - リクエスト/レスポンスの自動検証
- **モックサーバー** - 実装前にAPIを試せる

**「仕様書がそのまま動く」世界**

---

## スキーマ駆動開発 (API First)

```
1. OpenAPI仕様を書く
      ↓
2. チームでレビュー
      ↓
3. フロント: 仕様からコード自動生成
   バック:   仕様に沿って実装
      ↓
4. 自動テストで仕様との整合性を確認
```

フロントとバックエンドが**同時並行**で開発できる！

---

## FastAPI とは

Python製のモダンWeb APIフレームワーク

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}
```

たった数行でAPIが完成 🎉

---

## FastAPI の特徴

- **高速** - Starlette + Uvicorn ベース
- **簡単** - 学習コストが低い
- **型安全** - Pythonの型ヒントを活用
- **自動ドキュメント** - OpenAPI仕様を自動生成
- **バリデーション** - Pydantic による入力検証

---

## 型ヒントの力

FastAPIは**Pythonの型ヒント**がそのまま仕様になる

```python
@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}
```

この型ヒントから自動的に：

- `item_id` は整数（文字列が来たら422エラー）
- `q` はオプションの文字列パラメータ
- OpenAPIドキュメントが生成される

---

## Pydantic モデル

リクエスト/レスポンスの形を定義

```python
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    price: float
    is_offer: bool | None = None

@app.post("/items/")
def create_item(item: Item):
    return {"item_name": item.name, "item_price": item.price}
```

- JSON → Pythonオブジェクトの変換が自動
- バリデーションも自動（priceに文字列→エラー）
- APIドキュメントにスキーマが反映される

---

## 自動ドキュメント生成

FastAPIを起動するだけで2つのUIが使える

```
http://localhost:8000/docs     → Swagger UI
http://localhost:8000/redoc    → ReDoc
```

- コードを書くだけでドキュメントが**常に最新**
- ブラウザからAPIを**実際に実行**できる
- リクエスト/レスポンスの例も自動表示

**仕様書を手書きする時代は終わり！**

---

## レスポンスモデルの定義

```python
class UserResponse(BaseModel):
    id: int
    name: str
    email: str

@app.get("/users/{user_id}")
def get_user(user_id: int) -> UserResponse:
    return UserResponse(
        id=user_id,
        name="田中太郎",
        email="tanaka@example.com"
    )
```

返り値の型もドキュメントに反映される

---

## モダン開発スタイルとの親和性

--

### フロントエンド連携

```
FastAPI (Python)
  ↓ OpenAPI仕様を自動出力
openapi.json
  ↓ コード自動生成ツール
TypeScript クライアント (型付き！)
```

フロントエンドの型定義を手書きする必要なし

--

### CI/CD パイプライン

```
コード変更 → テスト → ビルド → デプロイ
               ↑
        OpenAPI仕様との整合性チェック
```

仕様とコードの乖離を自動検出

--

### Docker & クラウド

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY . .
RUN pip install fastapi uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0"]
```

コンテナ化も簡単。AWS / GCP / Azure へすぐデプロイ

---

## まとめ

| テーマ | ポイント |
|-------|---------|
| API | ソフトウェア同士の「窓口」 |
| OpenAPI | API仕様を標準フォーマットで記述 |
| FastAPI | 型ヒントから仕様を自動生成 |
| モダン開発 | スキーマ駆動で効率的な開発 |

**コード ↔ 仕様書の双方向連携がモダンAPI開発の強み**

---

## 参考資料

- [FastAPI公式ドキュメント](https://fastapi.tiangolo.com/ja/)
- [OpenAPI仕様](https://swagger.io/specification/)
- [Swagger UI](https://swagger.io/tools/swagger-ui/)
- [Pydantic公式](https://docs.pydantic.dev/)

---

# ありがとうございました

質問があればどうぞ！
