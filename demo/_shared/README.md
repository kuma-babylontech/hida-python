# reinfolib — 実データ取得・正規化基盤（Part1〜3 共通）

国土交通省「不動産情報ライブラリ」の取引価格情報取得 API (**XIT001**) から
データを取得し、**そのまま pandas で分析できる DataFrame** に整える共通モジュール。
Part2（回帰）・Part3（機械学習）のデモはここを経由してデータを読み込む。

## 使い方

```python
import reinfolib

df = reinfolib.load_dataframe()          # 分析レディな DataFrame
df[["PriceMan", "Area", "BuildingAge"]].describe()
```

- 環境変数 `REINFOLIB_API_KEY` が **あれば本番 API**、なければ実 API レスポンスに
  忠実なオフラインサンプル（`sample_xit001.csv`）で代替する。
- 本番取得を試す:

  ```bash
  export REINFOLIB_API_KEY=xxxxxxxx
  python reinfolib.py          # output/tokyo_mansion_analysis_ready.csv を書き出す
  ```

API キー申請: https://www.reinfolib.mlit.go.jp/api/request/ （無料・約5営業日）

## このモジュールが吸収する「実 API のクセ」

素朴に DataFrame 化すると分析コードが壊れる。`normalize()` が以下を吸収する。

| クセ | 実 API の値 | 対処 |
|------|-------------|------|
| 全項目が文字列 | `TradePrice="98000000"` | 数値列を `to_numeric` で数値化 |
| 建築年が**和暦** | `BuildingYear="平成20年"` | `2008` に変換し `BuildingAge` を算出 |
| 全角数字 | `Period="2025年第４四半期"` | 半角へ統一 |
| 変換不能な築年 | `BuildingYear="戦前"` | NaN にして分析対象から除外 |

付与される派生列: `BuildingYearSeireki` / `BuildingAge` / `PriceMan` / `UnitPriceMan`。

## ⚠ 実 API に「最寄駅・駅徒歩」は無い

XIT001 の出力項目に `NearestStation` / `TimeToNearestStation` は**存在しない**
（公式マニュアルの出力項目に駅情報なし）。旧サンプルデータにあった駅フィールドは
デモ用に創作されたもの。**駅徒歩を使った分析は実データではできない**ため、
面積（`Area`）・築年数（`BuildingAge`）・用途地域（`CityPlanning`）・構造（`Structure`）
など実在する項目で代替する。

実 API で使える主な項目:

| 項目 | 内容 | 用途の例 |
|------|------|---------|
| `TradePrice` / `PriceMan` | 取引価格（円／万円） | 目的変数 |
| `Area` | 面積（㎡） | 説明変数 |
| `BuildingYear` → `BuildingAge` | 建築年（和暦）→ 築年数 | 説明変数 |
| `Municipality` | 市区町村 | エリア分析 |
| `DistrictName` | 地区名 | エリア分析 |
| `FloorPlan` | 間取り | ワンルーム抽出 |
| `CityPlanning` | 用途地域 | カテゴリ分析 |
| `Structure` | 構造 | カテゴリ分析 |

## ファイル

| ファイル | 役割 |
|---------|------|
| `reinfolib.py` | 取得・正規化の本体（`fetch_transactions` / `normalize` / `load_dataframe`） |
| `00_generate_sample_data.py` | 実 API 形状に忠実なオフラインサンプルを生成 |
| `sample_xit001.csv` | オフラインサンプル（和暦・全角・文字列・駅情報なし） |
| `tests/` | 和暦変換・全角処理・型変換・API 呼び出しのテスト |

## テスト

```bash
pip install -r requirements.txt pytest
python -m pytest tests/ -q
```
