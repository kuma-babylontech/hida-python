"""
単回帰分析: 築年数だけで価格を説明する。

- OLS（最小二乗法）で回帰直線を求める
- 係数の解釈: 築年数 1年あたりの価格変化
- R²: モデルの説明力
- 散布図に回帰直線を重ねて可視化
"""

import sys
from pathlib import Path

import japanize_matplotlib  # noqa: F401
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.api as sm

# 共通の実データ取得基盤（demo/_shared/reinfolib.py）を読み込む。
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "_shared"))
import reinfolib  # noqa: E402

OUTPUT_DIR = Path(__file__).parent / "output"


def load_data() -> pd.DataFrame:
    """実データ取得基盤から分析レディな DataFrame を得る。

    鍵（REINFOLIB_API_KEY）があれば本番 API、無ければ実 API 形状のオフライン
    サンプル。BuildingAge / PriceMan / UnitPriceMan などの派生列は reinfolib が付与する。
    """
    return reinfolib.load_dataframe()


def run_simple_regression(df: pd.DataFrame) -> sm.regression.linear_model.RegressionResultsWrapper:
    X = df[["BuildingAge"]]
    X = sm.add_constant(X)
    y = df["PriceMan"]

    model = sm.OLS(y, X).fit()
    return model


def plot_regression(df: pd.DataFrame, model) -> None:
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.scatter(df["BuildingAge"], df["PriceMan"], alpha=0.4, label="物件データ")

    x_line = np.linspace(df["BuildingAge"].min(), df["BuildingAge"].max(), 100)
    y_line = model.params["const"] + model.params["BuildingAge"] * x_line
    ax.plot(x_line, y_line, color="red", linewidth=2, label="回帰直線")

    ax.set_xlabel("築年数")
    ax.set_ylabel("価格（万円）")
    ax.set_title("単回帰: 築年数 vs 価格")
    ax.legend()

    OUTPUT_DIR.mkdir(exist_ok=True)
    fig.savefig(OUTPUT_DIR / "01_simple_regression.png", dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved → {OUTPUT_DIR / '01_simple_regression.png'}")


def main():
    df = load_data()

    print("=" * 60)
    print("■ 単回帰分析: 築年数 → 価格")
    print("=" * 60)
    model = run_simple_regression(df)
    print(model.summary())

    print()
    print("-" * 60)
    print("■ 結果のポイント")
    print("-" * 60)
    coef = model.params["BuildingAge"]
    r2 = model.rsquared
    print(f"  築年数の係数: {coef:.1f} 万円/年")
    print(f"  → 築年数が 1年増えると価格は約 {abs(coef):.0f} 万円下がる")
    print(f"  R²: {r2:.3f} → 価格の {r2*100:.1f}% を築年数で説明できる")

    plot_regression(df, model)


if __name__ == "__main__":
    main()
