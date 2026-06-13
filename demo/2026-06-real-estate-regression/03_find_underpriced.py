"""
割安物件を見つける: 重回帰モデルの残差で相場との乖離を計算。

- predict() で各物件の「相場価格」を算出
- 残差 = 実際の価格 − 相場価格
- 残差が大きくマイナス = 割安
- 残差のヒストグラムでモデルの健全性を確認
"""

from datetime import datetime
from pathlib import Path

import japanize_matplotlib  # noqa: F401
import matplotlib.pyplot as plt
import pandas as pd
import statsmodels.api as sm

DATA_PATH = Path(__file__).parent.parent / "2026-04-real-estate-eda" / "data" / "tokyo_mansion.csv"
OUTPUT_DIR = Path(__file__).parent / "output"
CURRENT_YEAR = datetime.now().year


def load_data() -> pd.DataFrame:
    df = pd.read_csv(DATA_PATH)
    df["BuildingAge"] = CURRENT_YEAR - df["BuildingYear"].str.replace("年", "").astype(int)
    df["PriceMan"] = df["TradePrice"] / 10000
    return df


def main():
    df = load_data()

    X = df[["BuildingAge", "TimeToNearestStation", "Area"]]
    X = sm.add_constant(X)
    y = df["PriceMan"]
    model = sm.OLS(y, X).fit()

    df["predicted"] = model.predict(X)
    df["residual"] = df["PriceMan"] - df["predicted"]

    # 割安トップ10
    print("=" * 60)
    print("■ 割安物件トップ 10（残差が小さい順）")
    print("=" * 60)
    cols = ["Municipality", "NearestStation", "BuildingAge",
            "PriceMan", "predicted", "residual"]
    bargains = df.sort_values("residual").head(10)[cols].copy()
    bargains["predicted"] = bargains["predicted"].round(0)
    bargains["residual"] = bargains["residual"].round(0)
    print(bargains.to_string(index=False))

    # 割高トップ5
    print()
    print("=" * 60)
    print("■ 割高物件トップ 5（残差が大きい順）")
    print("=" * 60)
    overpriced = df.sort_values("residual", ascending=False).head(5)[cols].copy()
    overpriced["predicted"] = overpriced["predicted"].round(0)
    overpriced["residual"] = overpriced["residual"].round(0)
    print(overpriced.to_string(index=False))

    # 残差ヒストグラム
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.hist(df["residual"], bins=30, edgecolor="white", alpha=0.8)
    ax.axvline(0, color="red", linestyle="--", linewidth=1.5, label="残差 = 0")
    ax.set_xlabel("残差（万円）")
    ax.set_ylabel("件数")
    ax.set_title("残差の分布（0 中心 = モデル健全）")
    ax.legend()

    OUTPUT_DIR.mkdir(exist_ok=True)
    fig.savefig(OUTPUT_DIR / "02_residual_hist.png", dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"\nSaved → {OUTPUT_DIR / '02_residual_hist.png'}")


if __name__ == "__main__":
    main()
