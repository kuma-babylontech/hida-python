"""
重回帰分析: 複数の要因で価格を説明する。

- 築年数 + 駅徒歩 + 面積 の 3要因
- 各係数の解釈と p値の確認
- 単回帰との R² 比較
"""

from datetime import datetime
from pathlib import Path

import pandas as pd
import statsmodels.api as sm

DATA_PATH = Path(__file__).parent.parent / "2026-04-real-estate-eda" / "data" / "tokyo_mansion.csv"
CURRENT_YEAR = datetime.now().year


def load_data() -> pd.DataFrame:
    df = pd.read_csv(DATA_PATH)
    df["BuildingAge"] = CURRENT_YEAR - df["BuildingYear"].str.replace("年", "").astype(int)
    df["PriceMan"] = df["TradePrice"] / 10000
    return df


def run_multiple_regression(df: pd.DataFrame) -> sm.regression.linear_model.RegressionResultsWrapper:
    X = df[["BuildingAge", "TimeToNearestStation", "Area"]]
    X = sm.add_constant(X)
    y = df["PriceMan"]

    model = sm.OLS(y, X).fit()
    return model


def main():
    df = load_data()

    print("=" * 60)
    print("■ 重回帰分析: 築年数 + 駅徒歩 + 面積 → 価格")
    print("=" * 60)
    model = run_multiple_regression(df)
    print(model.summary())

    print()
    print("-" * 60)
    print("■ 各要因の影響（係数とp値）")
    print("-" * 60)
    for name in ["BuildingAge", "TimeToNearestStation", "Area"]:
        coef = model.params[name]
        pval = model.pvalues[name]
        sig = "✓ 有意" if pval < 0.05 else "✗ 有意でない"
        print(f"  {name:.<30} coef={coef:+.1f}  p値={pval:.4f}  {sig}")

    print()
    print("-" * 60)
    print("■ 結果のポイント")
    print("-" * 60)
    print(f"  R²: {model.rsquared:.3f} → 価格の {model.rsquared*100:.1f}% を説明できる")
    print()
    print("  解釈:")
    print(f"    築年数 1年増えると    → 約 {abs(model.params['BuildingAge']):.0f} 万円下がる")
    print(f"    駅徒歩 1分増えると    → 約 {abs(model.params['TimeToNearestStation']):.0f} 万円下がる")
    print(f"    面積 1㎡ 増えると     → 約 {abs(model.params['Area']):.0f} 万円上がる")


if __name__ == "__main__":
    main()
