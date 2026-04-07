# hida-python

飛騨高山Pythonの会のスライド資料を管理・閲覧するためのWebアプリケーションです。

## 公開URL

https://kuma-babylontech.github.io/hida-python/

## 技術スタック

| カテゴリ | 技術 |
|---------|------|
| フレームワーク | React 18 + Vite |
| 言語 | TypeScript |
| スタイリング | Tailwind CSS |
| スライド表示 | reveal.js（カスタム飛騨テーマ） |
| ルーティング | react-router-dom (HashRouter) |
| テスト | Vitest + React Testing Library |
| デプロイ | GitHub Actions → GitHub Pages |

## 開発コマンド

```bash
# 依存関係インストール
npm install

# 開発サーバー起動
npm run dev

# ビルド
npm run build

# テスト実行
npm run test

# Lint
npm run lint
```

## ディレクトリ構成

```
hida-python/
├── .github/workflows/    # GitHub Actions（自動デプロイ）
├── public/
│   └── slides/           # スライド用画像（ビルド出力にコピーされる）
├── src/
│   ├── components/       # Reactコンポーネント
│   ├── pages/            # ページコンポーネント
│   ├── hooks/            # カスタムフック
│   ├── types/            # 型定義
│   ├── styles/           # CSS（Tailwind + reveal.js テーマ）
│   └── utils/            # ユーティリティ関数
├── slides/               # Markdownスライドファイル
│   └── YYYY-MM-title/
│       ├── slide.md
│       └── assets/       # スライド用画像（ソース管理用）
├── demo/                 # デモコード
└── tests/                # テストファイル
```

## スライドの追加方法

1. `slides/YYYY-MM-title/` ディレクトリを作成
2. `slide.md` にフロントマターとスライド内容を記述
3. 画像を使用する場合は以下の両方に配置:
   - `slides/YYYY-MM-title/assets/` — ソース管理用
   - `public/slides/YYYY-MM-title/assets/` — ビルド出力用
4. コミット・プッシュで自動デプロイ

### スライドのフォーマット

```markdown
---
title: "スライドタイトル"
date: 2025-01-15
description: "スライドの概要説明"
tags:
  - タグ1
  - タグ2
author: "発表者名"
---

# スライド1

内容...

---

# スライド2

内容...
```

画像は `assets/` からの相対パスで参照できます（ビルド時に自動で絶対パスに変換）:

```markdown
![グラフ](assets/chart.png)
```

## スライド一覧

| 日付 | タイトル |
|------|---------|
| 2026-04-12 | [Pythonで学ぶ不動産データ分析 Part 1 — 探索的データ分析](slides/2026-04-real-estate-eda/) |
| 2026-02-08 | [OpenAPI × FastAPI 入門](slides/2026-02-openapi-fastapi/) |
| 2025-12-19 | [2025年 Python動向振り返り](slides/2025-12-python-recap/) |

## デモ

| スライド | デモ |
|---------|------|
| Pythonで学ぶ不動産データ分析 Part 1 | [demo/2026-04-real-estate-eda/](demo/2026-04-real-estate-eda/) |
| OpenAPI × FastAPI 入門 | [demo/2026-02-openapi-fastapi/](demo/2026-02-openapi-fastapi/) |

## ライセンス

MIT
