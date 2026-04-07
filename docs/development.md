# 開発ガイド

スライドの追加方法とアプリケーションの開発手順。

## スライドの追加方法

### 1. ディレクトリを作成

```bash
mkdir -p slides/YYYY-MM-title
```

### 2. slide.md を作成

フロントマターでメタデータを定義し、`---` でスライドを区切る。

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

### 3. 画像を使用する場合

画像は以下の **両方** に配置する:

```
slides/YYYY-MM-title/assets/image.png    ← ソース管理用
public/slides/YYYY-MM-title/assets/image.png  ← ビルド出力用
```

Markdown 内では `assets/` からの相対パスで参照できる（ビルド時に自動で絶対パスに変換）:

```markdown
![グラフ](assets/chart.png)
```

### 4. デモコードがある場合

`demo/YYYY-MM-title/` に配置する。

### 5. デプロイ

main ブランチにプッシュすると GitHub Actions で自動デプロイされる。

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
npm install     # 依存関係インストール
npm run dev     # 開発サーバー起動
npm run build   # ビルド
npm run test    # テスト実行
npm run lint    # Lint
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
