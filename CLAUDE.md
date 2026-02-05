# hida-python

飛騨高山Pythonの会のスライド資料を管理・閲覧するためのWebアプリケーション。GitHub Pagesで公開。

## 技術スタック

| カテゴリ | 技術 |
|---------|------|
| フレームワーク | React 18 + Vite |
| 言語 | TypeScript |
| スタイリング | Tailwind CSS |
| スライド表示 | reveal.js |
| ルーティング | react-router-dom (HashRouter) |
| テスト | Vitest + React Testing Library |
| デプロイ | GitHub Actions → GitHub Pages |

## ディレクトリ構成

```
hida-python/
├── .github/
│   └── workflows/
│       └── deploy.yml          # GitHub Pages自動デプロイ
├── public/
│   └── favicon.svg
├── src/
│   ├── components/
│   │   ├── common/             # 共通コンポーネント
│   │   ├── slides/             # スライド関連コンポーネント
│   │   └── layout/             # レイアウトコンポーネント
│   ├── pages/
│   │   ├── Home.tsx            # 一覧画面
│   │   └── SlideViewer.tsx     # スライド詳細画面
│   ├── hooks/                  # カスタムフック
│   ├── types/                  # 型定義
│   ├── utils/                  # ユーティリティ関数
│   ├── styles/                 # グローバルスタイル
│   ├── App.tsx
│   └── main.tsx
├── slides/                     # Markdownスライドファイル
│   └── YYYY-MM-title/
│       ├── slide.md            # スライド本体
│       └── assets/             # スライド用画像等
├── tests/
│   ├── components/
│   └── utils/
├── index.html
├── vite.config.ts
├── tsconfig.json
└── package.json
```

## スライドデータ構造

### Markdownファイル形式

スライドは `slides/YYYY-MM-title/slide.md` に配置。フロントマターでメタデータを定義。

```markdown
---
title: "Pythonの基礎"
date: 2025-01-15
description: "Python入門者向けの基礎文法解説"
tags:
  - 基礎
  - 文法
author: "発表者名"
---

# スライド1

内容...

---

# スライド2

内容...
```

### メタデータ型定義

```typescript
interface SlideMetadata {
  id: string;           // ディレクトリ名から自動生成
  title: string;        // スライドタイトル
  date: string;         // 発表日 (YYYY-MM-DD)
  description: string;  // 概要説明
  tags: string[];       // タグ一覧
  author?: string;      // 発表者名（任意）
}
```

## 画面仕様

### 一覧画面 (/)

- リスト形式でスライド一覧を表示
- 表示項目: タイトル、日付、説明、タグ
- タグによるフィルタリング機能
- 日付順（新しい順）でソート
- ダークモード対応

### 詳細画面 (/#/slides/:id)

- reveal.jsでスライドを表示
- キーボードナビゲーション対応
- フルスクリーン表示対応
- 一覧に戻るボタン

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

## GitHub Pagesデプロイ

### 自動デプロイ

`main` ブランチへのpush時にGitHub Actionsで自動デプロイ。

### デプロイフロー

1. 依存関係インストール
2. ビルド
3. GitHub Pagesにデプロイ

### 公開URL

`https://{username}.github.io/hida-python/`

## スタイルガイド

### テーマカラー

Tailwind CSSのカスタムカラーを使用。ダークモード対応。

```javascript
// tailwind.config.js
theme: {
  extend: {
    colors: {
      primary: {...},    // メインカラー
      secondary: {...},  // サブカラー
    }
  }
}
```

## 新しいスライドの追加手順

1. `slides/YYYY-MM-title/` ディレクトリを作成
2. `slide.md` にフロントマターとスライド内容を記述
3. 必要に応じて `assets/` に画像を配置
4. コミット・プッシュで自動デプロイ

## コーディング規約

### コンポーネント

- 関数コンポーネント + Hooks を使用
- Props の型は明示的に定義
- コンポーネントファイル名は PascalCase

### 状態管理

- ローカル状態は useState / useReducer
- 必要に応じて Context API を使用
- 外部状態管理ライブラリは使用しない

### テスト

- コンポーネントは React Testing Library でテスト
- ユーティリティ関数は単体テスト必須
- テストファイルは `*.test.ts(x)` 形式

## 注意事項

- reveal.js のスタイルとTailwind CSSの競合に注意
- GitHub Pagesはハッシュベースルーティングを使用（ヒストリーAPIは404になる）
