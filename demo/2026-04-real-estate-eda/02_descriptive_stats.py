"""
記述統計: データの全体像を数字で掴む。

- 平均 vs 中央値: 不動産価格は右に歪むので中央値が実態に近い
- 標準偏差: バラつきの大きさ ≒ リスクの大きさ
- pandas の describe() で一発確認
"""

from datetime import datetime
from pathlib import Path

import pandas as pd

DATA_PATH = Path(__file__).parent / "data" / "tokyo_mansion.csv"
CURRENT_YEAR = datetime.now().year


def load_data() -> pd.DataFrame:
    df = pd.read_csv(DATA_PATH)
    # 築年数を計算（現在年 − 建築年）
    df["BuildingAge"] = CURRENT_YEAR - df["BuildingYear"].str.replace("年", "").astype(int)
    # 価格を万円単位に変換
    df["PriceMan"] = df["TradePrice"] / 10000
    # 平米単価を万円単位に
    df["UnitPriceMan"] = df["UnitPrice"] / 10000
    return df


def main():
    df = load_data()

    # ==============================
    # 1. まずは describe() で全体像
    # ==============================
    print("=" * 60)
    print("■ 基本統計量 (describe)")
    print("=" * 60)
    cols = ["PriceMan", "Area", "BuildingAge", "TimeToNearestStation"]
    print(df[cols].describe().round(1).to_string())

    # ==============================
    # 2. 平均 vs 中央値
    # ==============================
    print()
    print("=" * 60)
    print("■ 平均 vs 中央値（取引価格・万円）")
    print("=" * 60)
    mean_price = df["PriceMan"].mean()
    median_price = df["PriceMan"].median()
    print(f"  平均:   {mean_price:,.0f} 万円")
    print(f"  中央値: {median_price:,.0f} 万円")
    print(f"  差:     {mean_price - median_price:+,.0f} 万円")
    print()
    print("  → 平均 > 中央値 なら、高額物件に引っ張られている")
    print("    不動産価格では中央値のほうが「普通の物件」の実態に近い")

    # ==============================
    # 3. エリア別の中央値
    # ==============================
    print()
    print("=" * 60)
    print("■ エリア別 中央価格（万円）")
    print("=" * 60)
    area_stats = (
        df.groupby("Municipality")["PriceMan"]
        .agg(["median", "count"])
        .sort_values("median", ascending=False)
    )
    area_stats.columns = ["中央価格", "件数"]
    print(area_stats.to_string())

    # ==============================
    # 4. 標準偏差 = バラつき = リスク
    # ==============================
    print()
    print("=" * 60)
    print("■ エリア別 標準偏差（価格のバラつき）")
    print("=" * 60)
    area_std = (
        df.groupby("Municipality")["PriceMan"]
        .agg(["std", "median"])
        .sort_values("std", ascending=False)
    )
    area_std["変動係数"] = (area_std["std"] / area_std["median"] * 100).round(1)
    area_std.columns = ["標準偏差", "中央価格", "変動係数(%)"]
    print(area_std.to_string())
    print()
    print("  → 変動係数が大きい = 価格のバラつきが大きい = リスクが高い")


if __name__ == "__main__":
    main()
