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

### 発表者の個人的な動機

- 実は私、不動産投資をしています
- でも正直、物件選びは **「勘」と「営業トーク」頼み**
- 統計はほぼ初心者 — 数字で語れるようになりたい

→ せっかくなので勉強過程を勉強会のネタにしました

--

### なぜこの題材がPython学習に向くか

- **公開API** があり誰でも同じデータで試せる（国交省）
- 価格・面積・築年数など **数値と categorical が混在**
- pandas / matplotlib / seaborn の練習にちょうどいい粒度
- 不動産に興味がなくても **EDAの型** は他分野に応用できる

--

### データで答えたい問い（発表者の関心）

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

--

### ⚠ 今回は API キーが間に合いませんでした

- 申請済みだが **発行待ち**（約5営業日かかる）
- なので今日は **API をモック** してデモします
- `unittest.mock` で `requests.get` を差し替え
- レスポンスは本物の仕様に合わせた **サンプルデータ（500件）**

→ キーが届いたら同じコードが本番 API にそのまま通る設計

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

--

### そもそも「モック」って何？

**モック = 本物のふりをするニセモノ**

- 映画の撮影で使う「小道具の電話」みたいなもの
- 見た目や使い方は本物と同じ
- でも中身は自分で作った簡単なもの

今回は「ネットにつないでデータを取ってくる関数」の
ふりをしてくれるニセモノを作ります

--

### コード解説① 本物の代わりにニセモノを使う

```python
from unittest.mock import patch

with patch("requests.get", side_effect=_mock_api_response):
    df = fetch_transactions(2025, 1)
```

- `requests.get` = 本来ネットにアクセスする関数
- `patch("requests.get", ...)` = その関数を **一時的に別物に入れ替える**
- `side_effect=_mock_api_response` = 「呼ばれたらこの自作関数を動かしてね」
- `with` ブロックの中だけ入れ替わり、外に出ると元通り

→ **本物の API を呼ばずに、同じコードでテストできる**

--

### コード解説② ニセモノの中身を作る

```python
def _mock_api_response(*args, **kwargs):
    params = kwargs.get("params", {})
    target = f"{params['year']}年第{params['quarter']}四半期"
    records = [r for r in _load_sample_records()
               if r["Period"] == target]
    ...
```

- `kwargs` = 呼び出し側が渡してきた引数（辞書の形）
- そこから `year` と `quarter` を取り出す
- サンプルデータの中から **その期間に合うものだけ** を選ぶ
- リスト内包表記: `[x for x in リスト if 条件]` は
  「条件に合うものを集めた新しいリストを作る」という意味

→ 本物の API と同じ「期間を指定するとその期間のデータが返る」動きを再現

--

### コード解説③ ニセモノのレスポンスを組み立てる

```python
mock_resp = MagicMock(spec=requests.Response)
mock_resp.status_code = 200
mock_resp.json.return_value = {"status": "OK", "data": records}
return mock_resp
```

- `MagicMock` = **どんなメソッドも持ってる便利なニセモノ**
- `spec=requests.Response` =「本物と同じ形に揃えて」というお願い
- `status_code = 200` → 「成功しましたよ」という意味
- `json.return_value = ...` → 「`.json()` が呼ばれたらこの辞書を返してね」
- 本物のレスポンスは `{"status": "OK", "data": [...]}` という形なのでそれに合わせる

--

### コード解説④ 本番とテストを切り替える

```python
API_KEY = os.environ.get("REINFOLIB_API_KEY", "")
USE_MOCK = not API_KEY
```

- `os.environ.get(...)` = パソコンの環境変数を読む
- キーがあれば本番、なければ自動でモック
- **`fetch_transactions` の中身は 1 行も変えなくていい**
- キーが届いたらターミナルで

  ```bash
  export REINFOLIB_API_KEY=xxxxxxx
  ```

  とするだけで本物の API に切り替わる

--

### なぜわざわざモックを使うの？

| もしモックがなかったら | モックがあると |
|---|---|
| API キーが届くまで何もできない | **今日から書ける** |
| ネットがないと動かない | **オフラインでも動く** |
| API が壊れたらテストも落ちる | **安定して動く** |
| 使いすぎると料金やエラーが心配 | **何回でも無料** |

→ 外部サービスを使うコードを書くときの **お決まりのやり方**

---

## 記述統計

数字で全体像をつかむ

--

### pandas の describe() が最強

```python
import pandas as pd

df = pd.read_csv("tokyo_mansion.csv")
df["BuildingAge"] = 2025 - df["BuildingYear"].str.replace("年", "").astype(int)
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

### そもそも DataFrame って何？

**DataFrame = Excel の表みたいなもの**

```
    TradePrice  BuildingYear  Municipality
0   15,000,000      1995年        新宿区
1   22,000,000      2010年        港区
2   ...
```

- 横が「行」（1 物件 = 1 行）
- 縦が「列」（価格、築年など項目ごと）
- pandas はこの表を Python から簡単に触れるライブラリ

--

### コード解説① 新しい列を作る

```python
df["BuildingAge"] = 2025 - df["BuildingYear"].str.replace("年", "").astype(int)
df["PriceMan"]    = df["TradePrice"] / 10000
```

やっていること:

1. `BuildingYear` は `"1995年"` のような **文字** なので計算できない
2. `.str.replace("年", "")` で `"年"` を消して `"1995"` にする
3. `.astype(int)` で文字を数字に変換 → `1995`
4. `2025 - 1995` で築年数が出る

ポイント:

- `df["新しい名前"] = ...` と書くと **列がまるごと 1 本追加される**
- `for` ループを書かなくても **全行まとめて計算** してくれる（pandas の魔法）
- 円は桁が大きいので `/ 10000` で万円に直すと読みやすい

--

### コード解説② describe() は最初のごあいさつ

```python
df[["PriceMan", "Area", "BuildingAge"]].describe()
```

- `df[["列A", "列B"]]` = **見たい列だけを選ぶ**
  （カッコが 2 重なのは「リストを渡してる」から）
- `.describe()` = 選んだ列について **8 つの数字をまとめて教えてくれる**

| 行 | 何の数字？ | どう見る？ |
|---|---|---|
| count | 件数 | データが何件あるか |
| mean | 平均 | だいたいの真ん中 |
| std | バラつき | 数字がどれくらい散らばっているか |
| min / max | 最小・最大 | 一番安い / 高い物件 |
| 25% / 50% / 75% | 順番に並べた時の区切り | **50% が中央値** |

→ 新しいデータを見るときは **まず describe() を叩く**、が合言葉

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

### コード解説③ 平均と中央値の出し方

```python
mean_price   = df["PriceMan"].mean()
median_price = df["PriceMan"].median()
print(f"平均:   {mean_price:,.0f} 万円")
print(f"差:     {mean_price - median_price:+,.0f} 万円")
```

- `df["PriceMan"]` = 価格の列だけを取り出す
- そこに `.mean()` や `.median()` を付ければ計算完了
- 本当にこれだけ。for ループも、合計 ÷ 件数 も書かなくていい

**f-string の小ワザ**:

- `{数字:,.0f}` → `1,300` のように 3 桁ごとにカンマが入る
- `{数字:+,.0f}` → `+131` のように符号が付く

→ 結果を「見やすく」出すだけで分析のストレスが激減

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

--

### コード解説④ 区ごとにまとめて集計する

```python
area_std = (
    df.groupby("Municipality")["PriceMan"]
      .agg(["std", "median"])
      .sort_values("std", ascending=False)
)
```

**イメージ**: 500 件の物件カードを「港区の山・新宿区の山…」と
区ごとに分けて、山ごとに統計を出す感じ

- `groupby("Municipality")` = **市区町村ごとに仲間分け**
- `["PriceMan"]` = その中で価格の列だけ見る
- `.agg(["std", "median"])` = バラつきと中央値を **同時に計算**
- `.sort_values("std", ...)` = バラつきが大きい順に並べ替え

→ Excel のピボットテーブルに近いことが 4 行で書ける

--

### コード解説⑤ バラつきの「比較」は割り算で

```python
area_std["変動係数"] = area_std["std"] / area_std["median"] * 100
```

**なぜ割るのか？**

- 港区の価格が 2,000 万、板橋区が 800 万
- 当然、港区のほうが **金額のバラつき(std)も大きく出る**
- それだと「港区のほうがリスク高い！」と勘違いしそう

でも本当に知りたいのは「中央値に対して **何%** ブレるか」

- `std ÷ median × 100` = **変動係数**（%）
- これなら金額の大小に関係なく、**公平に比べられる**

→ 物差しを揃えるだけでデータの見え方が変わる、という統計の基本

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
