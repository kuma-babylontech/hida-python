"""
可視化: データを「目で見て」パターンを発見する。

matplotlib + seaborn で4種類のグラフを描く:
1. ヒストグラム — 価格帯の分布
2. 散布図 — 築年数 vs 価格、駅距離 vs 価格
3. 箱ひげ図 — エリア別の価格比較
4. 相関行列ヒートマップ — 変数間の関係を俯瞰
"""

from pathlib import Path

import japanize_matplotlib  # noqa: F401
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

DATA_PATH = Path(__file__).parent / "data" / "tokyo_mansion.csv"
OUTPUT_DIR = Path(__file__).parent / "output"


def load_data() -> pd.DataFrame:
    df = pd.read_csv(DATA_PATH)
    df["BuildingAge"] = 2025 - df["BuildingYear"].str.replace("年", "").astype(int)
    df["PriceMan"] = df["TradePrice"] / 10000
    df["UnitPriceMan"] = df["UnitPrice"] / 10000
    return df


def plot_histogram(df: pd.DataFrame):
    """1. 価格分布のヒストグラム"""
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.hist(df["PriceMan"], bins=30, color="#4C78A8", edgecolor="white", alpha=0.8)
    ax.axvline(df["PriceMan"].mean(), color="red", linestyle="--", label=f'平均: {df["PriceMan"].mean():,.0f}万円')
    ax.axvline(df["PriceMan"].median(), color="orange", linestyle="--", label=f'中央値: {df["PriceMan"].median():,.0f}万円')
    ax.set_xlabel("取引価格（万円）")
    ax.set_ylabel("件数")
    ax.set_title("東京23区 中古ワンルーム 取引価格の分布")
    ax.legend()
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "01_histogram.png", dpi=150)
    print("Saved: 01_histogram.png")
    plt.close()


def plot_scatter(df: pd.DataFrame):
    """2. 築年数・駅距離と価格の散布図"""
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # 築年数 vs 価格
    axes[0].scatter(df["BuildingAge"], df["PriceMan"], alpha=0.4, s=20, color="#4C78A8")
    axes[0].set_xlabel("築年数（年）")
    axes[0].set_ylabel("取引価格（万円）")
    axes[0].set_title("築年数 vs 取引価格")

    # 駅距離 vs 価格
    axes[1].scatter(df["TimeToNearestStation"], df["PriceMan"], alpha=0.4, s=20, color="#F58518")
    axes[1].set_xlabel("最寄り駅 徒歩（分）")
    axes[1].set_ylabel("取引価格（万円）")
    axes[1].set_title("駅距離 vs 取引価格")

    fig.suptitle("価格に影響する要因を散布図で確認", fontsize=14)
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "02_scatter.png", dpi=150)
    print("Saved: 02_scatter.png")
    plt.close()


def plot_boxplot(df: pd.DataFrame):
    """3. エリア別の価格比較（箱ひげ図）"""
    # 件数上位10区に絞る
    top_areas = df["Municipality"].value_counts().head(10).index
    df_top = df[df["Municipality"].isin(top_areas)].copy()

    # 中央値順にソート
    order = df_top.groupby("Municipality")["PriceMan"].median().sort_values(ascending=False).index

    fig, ax = plt.subplots(figsize=(12, 5))
    sns.boxplot(data=df_top, x="Municipality", y="PriceMan", hue="Municipality", order=order, ax=ax, palette="Blues_r", legend=False)
    ax.set_xlabel("区")
    ax.set_ylabel("取引価格（万円）")
    ax.set_title("エリア別 中古ワンルーム価格（上位10区）")
    plt.xticks(rotation=45)
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "03_boxplot.png", dpi=150)
    print("Saved: 03_boxplot.png")
    plt.close()


def plot_correlation(df: pd.DataFrame):
    """4. 相関行列ヒートマップ"""
    cols = {
        "PriceMan": "取引価格",
        "Area": "面積",
        "BuildingAge": "築年数",
        "TimeToNearestStation": "駅徒歩",
        "UnitPriceMan": "平米単価",
    }
    df_corr = df[list(cols.keys())].rename(columns=cols)
    corr = df_corr.corr()

    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="RdBu_r", center=0, ax=ax, square=True)
    ax.set_title("変数間の相関行列")
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "04_correlation.png", dpi=150)
    print("Saved: 04_correlation.png")
    plt.close()


def main():
    OUTPUT_DIR.mkdir(exist_ok=True)
    df = load_data()
    print(f"Loaded {len(df)} records\n")

    plot_histogram(df)
    plot_scatter(df)
    plot_boxplot(df)
    plot_correlation(df)

    print(f"\nAll charts saved to {OUTPUT_DIR}/")


if __name__ == "__main__":
    main()
