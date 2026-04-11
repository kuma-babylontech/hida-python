"""
02_descriptive_stats.py のテスト。

load_data() の前処理（文字列 → 数値変換、単位変換、派生カラム追加）が
正しく動いていることを確認する。
"""

import pandas as pd
import pytest


class TestLoadData:
    @pytest.fixture(scope="class")
    def df(self, descriptive_mod):
        return descriptive_mod.load_data()

    def test_is_dataframe_with_rows(self, df):
        assert isinstance(df, pd.DataFrame)
        assert len(df) > 0

    def test_derived_columns_exist(self, df):
        for col in ("BuildingAge", "PriceMan", "UnitPriceMan"):
            assert col in df.columns

    def test_building_age_is_integer_like(self, df):
        # "1995年" のような文字列が int に変換されている
        assert pd.api.types.is_integer_dtype(df["BuildingAge"])
        assert (df["BuildingAge"] >= 0).all()
        assert (df["BuildingAge"] <= 100).all()

    def test_price_man_is_trade_price_divided_by_10000(self, df):
        expected = df["TradePrice"] / 10000
        pd.testing.assert_series_equal(
            df["PriceMan"], expected, check_names=False
        )

    def test_building_age_formula(self, df):
        # 生データから再計算して一致すること
        years = df["BuildingYear"].str.replace("年", "").astype(int)
        pd.testing.assert_series_equal(
            df["BuildingAge"], 2025 - years, check_names=False
        )


class TestDescribeIntegration:
    """スライドで見せる `describe()` 出力が期待した形になるか。"""

    def test_describe_has_eight_rows(self, descriptive_mod):
        df = descriptive_mod.load_data()
        desc = df[["PriceMan", "Area", "BuildingAge"]].describe()
        assert list(desc.index) == [
            "count", "mean", "std", "min", "25%", "50%", "75%", "max",
        ]

    def test_median_less_than_mean_for_right_skewed_price(self, descriptive_mod):
        # 不動産価格は右に歪んでいるはず: 平均 > 中央値
        df = descriptive_mod.load_data()
        assert df["PriceMan"].mean() > df["PriceMan"].median()
