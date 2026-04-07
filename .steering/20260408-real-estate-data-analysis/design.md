# 第1回 設計: データ収集と探索的分析

## 成果物

1. `slides/2026-04-real-estate-eda/slide.md` — スライド本体
2. `demo/2026-04-real-estate-eda/` — デモ用 Python コード

## スライド構成（20分）

1. イントロ（2分）
   - シリーズ概要、なぜ不動産 × データ分析か
   - 「勘で選ぶ」から「数字で判断する」へ

2. データの入手（3分）
   - 不動産情報ライブラリ API の紹介
   - Python でデータを取得するデモ

3. データの全体像を掴む — 記述統計（5分）
   - 平均 vs 中央値（不動産価格は歪むので中央値が重要）
   - 標準偏差（バラつきの大きさ = リスク）
   - pandas の describe() で一発確認

4. データを目で見る — 可視化（7分）
   - ヒストグラム: 価格帯の分布
   - 散布図: 築年数 vs 価格、駅距離 vs 価格
   - 箱ひげ図: エリア別の価格比較
   - 相関行列ヒートマップ: 変数間の関係を俯瞰

5. まとめと次回予告（3分）
   - 今日わかったこと
   - 次回: 回帰分析で「なぜその価格なのか」を解き明かす

## デモコード構成

```
demo/2026-04-real-estate-eda/
├── requirements.txt          # 依存パッケージ
├── 01_fetch_data.py          # API からデータ取得
├── 02_descriptive_stats.py   # 記述統計
├── 03_visualization.py       # 可視化
└── data/                     # 取得済みサンプルデータ（API 制限対策）
    └── tokyo_mansion.csv
```

## データ仕様

### 不動産情報ライブラリ API

- エンドポイント: `https://www.reinfolib.mlit.go.jp/ex-api/external/XIT002`
- 対象: 不動産取引価格情報
- フィルタ条件:
  - 都道府県: 東京都（13）
  - 種類: 中古マンション等
  - 期間: 直近数四半期
- API キーが必要（無料登録）

### 使用する主なカラム

| カラム | 内容 | 分析での用途 |
|-------|------|-------------|
| TradePrice | 取引価格 | 目的変数 |
| Area | 面積（㎡） | 説明変数 |
| BuildingYear | 建築年 | 築年数を算出 |
| NearestStation | 最寄り駅 | エリア分析 |
| TimeToNearestStation | 駅徒歩分 | 説明変数 |
| FloorPlan | 間取り | ワンルーム抽出 |
| Municipality | 市区町村 | エリア分析 |

## 技術選定

| ライブラリ | 用途 |
|-----------|------|
| requests | API 通信 |
| pandas | データ操作 |
| matplotlib | 基本グラフ |
| seaborn | 統計的可視化 |
| japanize-matplotlib | 日本語フォント対応 |
