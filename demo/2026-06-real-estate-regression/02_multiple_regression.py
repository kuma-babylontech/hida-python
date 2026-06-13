"""
重回帰分析: 複数の要因で価格を説明する。

- 面積 + 築年数 の 2要因
- 各係数の解釈と p値の確認
- 単回帰との R² 比較

※ 実 API (XIT001) には最寄駅・駅徒歩の項目が無いため、説明変数は実在する
  面積・築年数を使う。データは共通基盤 reinfolib 経由で取得する。
"""

import sys
from pathlib import Path

import pandas as pd
import statsmodels.api as sm

# 共通の実データ取得基盤（demo/_shared/reinfolib.py）を読み込む。
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "_shared"))
import reinfolib  # noqa: E402

#: 重回帰の説明変数（実 API に存在する数値項目）。
FEATURES = ["Area", "BuildingAge"]


def load_data() -> pd.DataFrame:
    """実データ取得基盤から分析レディな DataFrame を得る。"""
    return reinfolib.load_dataframe()


def run_multiple_regression(df: pd.DataFrame) -> sm.regression.linear_model.RegressionResultsWrapper:
    X = df[FEATURES]
    X = sm.add_constant(X)
    y = df["PriceMan"]

    model = sm.OLS(y, X).fit()
    return model


def main():
    df = load_data()

    print("=" * 60)
    print("■ 重回帰分析: 面積 + 築年数 → 価格")
    print("=" * 60)
    model = run_multiple_regression(df)
    print(model.summary())

    print()
    print("-" * 60)
    print("■ 各要因の影響（係数とp値）")
    print("-" * 60)
    for name in FEATURES:
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
    print(f"    面積 1㎡ 増えると     → 約 {abs(model.params['Area']):.0f} 万円上がる")
    print(f"    築年数 1年増えると    → 約 {abs(model.params['BuildingAge']):.0f} 万円下がる")


if __name__ == "__main__":
    main()
