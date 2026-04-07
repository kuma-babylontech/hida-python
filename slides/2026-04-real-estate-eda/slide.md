---
title: "Pythonで学ぶ不動産データ分析 Part 1 — 探索的データ分析"
date: 2026-04-12
description: "東京の中古ワンルームマンション取引データを題材に、pandasによる記述統計とmatplotlib/seabornによるデータ可視化の基礎を学びます。"
tags:
  - データ分析
  - 統計
  - pandas
  - 可視化
  - 不動産
author: "kuma"
---

# Pythonで学ぶ<br>不動産データ分析

## Part 1: 探索的データ分析

飛騨高山Pythonの会 2026年4月

---

## 今日のアジェンダ

1. シリーズ概要
2. データの入手方法
3. 記述統計 — 数字で全体像をつかむ
4. 可視化 — 目でパターンを見つける
5. まとめと次回予告

---

## このシリーズについて

全3回で **Python × 統計 × AI** を学ぶ

| 回 | テーマ | 統計トピック |
|---|---|---|
| **① 4月** | **探索的データ分析** | **記述統計・可視化** |
| ② 5月 | 回帰分析 | 単回帰・重回帰・p値 |
| ③ 6月 | 機械学習 | ランダムフォレスト |

題材: **東京23区 中古ワンルームマンション**

---

## なぜ不動産 × データ分析？

--

### 「勘」で選んでいませんか？

- 不動産屋に勧められるまま購入
- 「駅近だから大丈夫」という思い込み
- 利回りの数字だけを見て判断

--

### データで判断できること

- このエリアの **相場** はいくら？
- 築年数で価格は **どれくらい下がる**？
- 本当に **割安** な物件はどれ？

→ 今日はその第一歩「データを見る力」を身につけます

---

## データの入手

--

### 不動産情報ライブラリ（国交省）

https://www.reinfolib.mlit.go.jp/

- 国土交通省が提供する **オープンデータ**
- 実際の不動産取引価格情報を収録
- **API** でプログラムから取得可能（無料・要申請）

--

### API の使い方

```python
import requests

API_URL = "https://www.reinfolib.mlit.go.jp/ex-api/external/XIT001"

resp = requests.get(API_URL, headers={
    "Ocp-Apim-Subscription-Key": "YOUR_API_KEY"
}, params={
    "year": "2025",
    "quarter": "1",
    "area": "13",       # 東京都
})

data = resp.json()
```

API キー申請: 約5営業日（無料）

--

### 今日使うデータ

API レスポンスと同じ形式のサンプルデータ（500件）

| カラム | 内容 |
|-------|------|
| TradePrice | 取引価格（円） |
| Area | 面積（㎡） |
| BuildingYear | 建築年 |
| Municipality | 市区町村 |
| NearestStation | 最寄り駅 |
| TimeToNearestStation | 駅徒歩（分） |

---

## 記述統計

数字で全体像をつかむ

--

### pandas の describe() が最強

```python
import pandas as pd

df = pd.read_csv("tokyo_mansion.csv")
df["BuildingAge"] = 2025 - df["BuildingYear"]
df["PriceMan"] = df["TradePrice"] / 10000

df[["PriceMan", "Area", "BuildingAge"]].describe()
```

```
          PriceMan   Area  BuildingAge
count      500.0   500.0      500.0
mean      1299.7    23.1       22.0   ← 平均
std        576.4     4.1       10.5   ← 標準偏差
min        495.5    16.0        5.0
25%        841.6    19.4       13.0
50%       1168.7    22.9       21.0   ← 中央値
75%       1658.7    26.7       32.0
max       3349.8    30.0       40.0
```

--

### 平均 vs 中央値

```
平均:   1,300 万円
中央値: 1,169 万円
差:     +131 万円
```

**平均 > 中央値** → 高額物件に引っ張られている

不動産価格のような **右に歪んだ分布** では
**中央値** のほうが「普通の物件」の実態に近い

--

### 標準偏差 = バラつき = リスク

```
港区:   中央価格 2,011万円  変動係数 30.2%
板橋区: 中央価格   820万円  変動係数 24.9%
中野区: 中央価格   946万円  変動係数 55.4%  ← !?
```

**変動係数**（標準偏差 ÷ 中央値）で比較すると…

- 板橋区: 価格が安定 → リスク低め
- 中野区: 同じ区でも価格差が大きい → 物件選びが重要

---

## 可視化

目でパターンを見つける

--

### 1. ヒストグラム — 分布を見る

```python
import matplotlib.pyplot as plt

plt.hist(df["PriceMan"], bins=30)
plt.axvline(df["PriceMan"].mean(), color="red",
            linestyle="--", label="平均")
plt.axvline(df["PriceMan"].median(), color="orange",
            linestyle="--", label="中央値")
plt.legend()
```

→ 右裾が長い（＝高額物件が少数ある）ことが一目でわかる

--

### ヒストグラムの結果

![価格分布](assets/01_histogram.png)

平均と中央値のズレ = **分布の歪み** が可視化できた

--

### 2. 散布図 — 関係を見る

```python
fig, axes = plt.subplots(1, 2)

axes[0].scatter(df["BuildingAge"], df["PriceMan"])
axes[0].set_xlabel("築年数")

axes[1].scatter(df["TimeToNearestStation"], df["PriceMan"])
axes[1].set_xlabel("駅徒歩（分）")
```

--

### 散布図の結果

![散布図](assets/02_scatter.png)

- 築年数が増えると価格は **下がる傾向**（左図）
- 駅から遠いと価格は **やや下がる**（右図）

→ 次回の回帰分析で「どれくらい影響するか」を数値化します

--

### 3. 箱ひげ図 — エリアを比較する

```python
import seaborn as sns

sns.boxplot(data=df, x="Municipality", y="PriceMan")
```

--

### 箱ひげ図の結果

![箱ひげ図](assets/03_boxplot.png)

- 箱 = 25%〜75% の範囲（物件の半数がここに入る）
- ○ = 外れ値（極端に高い/安い物件）
- 箱の大きさ = バラつき → エリアごとのリスクが見える

--

### 4. 相関行列 — 変数間の関係を俯瞰

```python
corr = df[["PriceMan", "Area", "BuildingAge",
           "TimeToNearestStation"]].corr()
sns.heatmap(corr, annot=True, cmap="RdBu_r")
```

--

### 相関行列の結果

![相関行列](assets/04_correlation.png)

| 相関係数 | 意味 |
|---------|------|
| +1 に近い | 一方が増えるともう一方も増える |
| −1 に近い | 一方が増えるともう一方は減る |
| 0 に近い | 関係が薄い |

築年数 vs 価格 = **-0.42**（築年数が増えると価格は下がる）

---

## 今日のまとめ

--

### 学んだこと

| 概念 | 不動産での意味 |
|------|-------------|
| 中央値 | 「普通の物件」の価格を知る |
| 標準偏差 | エリアのリスク（バラつき）を測る |
| ヒストグラム | 価格帯の分布を把握する |
| 散布図 | 築年数・駅距離と価格の関係を見る |
| 相関行列 | どの要因が価格に効くか俯瞰する |

--

### 使ったツール

```bash
pip install pandas matplotlib seaborn japanize-matplotlib
```

```python
df.describe()          # 記述統計
plt.hist()             # ヒストグラム
plt.scatter()          # 散布図
sns.boxplot()          # 箱ひげ図
sns.heatmap(df.corr()) # 相関行列
```

--

### 次回予告（5月）

## 回帰分析で価格の構造を理解する

- 「築年数が1年増えると価格はいくら下がる？」
- 「駅徒歩1分の価値は何万円？」
- 統計的に「割安な物件」を見つける方法

---

## デモコード・資料

GitHub で公開しています

`demo/2026-04-real-estate-eda/`

```
00_generate_sample_data.py  # サンプルデータ生成
01_fetch_data.py            # API からデータ取得
02_descriptive_stats.py     # 記述統計
03_visualization.py         # 可視化
```

---

# ありがとうございました

質問・フィードバック歓迎です！
