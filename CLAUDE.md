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
│       └── assets/             # スライド用画像（編集元。配信は public/slides/ 側）
├── demo/                       # スライド付属のPythonデモ（Web本体とは独立）
│   ├── YYYY-MM-title/          # 各回のデモ（番号付きスクリプト + tests/）
│   └── _shared/                # シリーズ共通の取得・正規化基盤（reinfolib）
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

# テスト（カバレッジ / UI）
npm run test:coverage
npm run test:ui
```

> スペルチェック設定は `cspell.json` を参照。

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

Tailwind CSS **v4**（`@tailwindcss/vite` プラグイン）を使用。`tailwind.config.js` は**存在しない**。
テーマは `src/styles/index.css` の `@theme` ブロックにCSS変数として定義する。

- カラー: `primary-50`〜`primary-950`、`python-blue` / `python-yellow`、`hida-cedar` / `hida-cedar-light` / `hida-ink` / `hida-paper` / `hida-warm`
- ダークモード: `@custom-variant dark (&:where(.dark, .dark *))`（class方式。`src/hooks/useTheme.ts` で切替）
- フォント: `--font-display`（明朝）/ `--font-body`（ゴシック）/ `--font-mono`

> 色・フォントを追加・変更する場合は `tailwind.config.js` ではなく `src/styles/index.css` の `@theme` を編集する。

## 新しいスライドの追加手順

1. `slides/YYYY-MM-title/` ディレクトリを作成
2. `slide.md` にフロントマターとスライド内容を記述
3. 画像は `slides/YYYY-MM-title/assets/`（編集元）と `public/slides/YYYY-MM-title/assets/`（**実際の配信元**）の**両方**に置く。`src/utils/slides.ts` が `![](assets/x)` を `${BASE_URL}slides/<id>/assets/x` へ変換するため、`public/slides/` 側に無いと表示されない
4. コミット・プッシュで自動デプロイ

## デモコード（`demo/`）

一部のスライドには、発表で見せるPythonデモが `demo/YYYY-MM-title/` に付属する（Web本体とは独立。デプロイ対象外で、GitHubで閲覧・各自ローカル実行する想定）。

- スクリプトは実行順に**番号始まり**（`01_*.py` 等）。数字始まりで通常 `import` できないため、`tests/conftest.py` は `importlib.util` で動的ロードしてフィクスチャ化する
- 各デモは自前の `requirements.txt` と `.venv`（gitignore）を持つ。生成物は `demo/*/output/` に出力（gitignore 済み）
- **`demo/_shared/reinfolib.py`** = 不動産シリーズ（Part1〜3）共通の実データ取得・正規化基盤。国交省「不動産情報ライブラリ」XIT001 API を扱う。詳細は `demo/_shared/README.md`
  - 環境変数 `REINFOLIB_API_KEY` があれば本番API、無ければ**同梱の実データスナップショット**（`tokyo_oneroom_2024.csv`／東京・2024通年・中古ワンルーム、国交省オープンデータ）にフォールバック。どちらも同じ正規化を通し、鍵の有無で結果が変わらないよう `load_dataframe` の既定年は 2024 とスナップショットに揃えてある（合成サンプルは廃止済み）
  - 実APIのクセを `normalize()` で吸収: **全項目が文字列** / **建築年は `"YYYY年"`（マンションはほぼ西暦。和暦 `平成20年` も両対応）→ 築年数 = 実行年 − 西暦** / **全角数字**（`第４四半期`）/ `戦前`・空値は NaN 化
  - **XIT001 に最寄駅・駅徒歩の項目は無い**（`NearestStation`/`TimeToNearestStation` は存在しない）。駅を使った分析は不可で、面積・築年数・用途地域・構造などで代替する
  - 実データの落とし穴: **マンションは `UnitPrice`/`PricePerUnit` が空**（㎡単価は取れない）。間取り `１Ｋ` のまま 135㎡ 等の**誤登録**が混じるため、ワンルーム抽出は 1R/1K に加え**面積 10〜40㎡**でも絞っている
- データ分析スライドの数字（係数・R²・相場式）は**デモの実行結果と一致させる**。数値を変えたら必ずデモを再実行し、図も再生成して `slides/<id>/assets/` と `public/slides/<id>/assets/` の両方に置く。築年数は実行年（`datetime.now().year`）依存なので、年をまたぐと微妙に変わる

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
- スライドは `import.meta.glob('/slides/**/slide.md', { query: '?raw' })` で**ビルド時にバンドル**される（実行時fetchではない）。新規スライドは再ビルドで反映。`vite.config.ts` の `assetsInclude: ['**/*.md']` が前提
- スライド内画像は `![](assets/xxx)` と相対指定する → `src/utils/slides.ts` が `BASE_URL` 付き絶対パスへ自動変換
- フロントマター解析は `src/utils/slides.ts` の自前簡易パーサ（`gray-matter` は依存にあるが未使用）。ネストや複雑なYAMLは非対応で、`title` / `date` / `description` / `tags`（リスト）/ `author` のみ想定
- パスエイリアス `@` → `src`（`vite.config.ts`）。`base` は `/hida-python/`
