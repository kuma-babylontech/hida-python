"""
回帰分析デモスクリプトのテスト。

- load_data が正しく前処理されたDataFrameを返すこと
- 単回帰モデルの基本性質（係数の符号、R²の範囲）
- 重回帰モデルで説明力が単回帰より改善すること
- 残差の計算が正しいこと
"""

import pandas as pd
import pytest


class TestLoadData:
    def test_returns_dataframe(self, simple_reg_mod):
        df = simple_reg_mod.load_data()
        assert isinstance(df, pd.DataFrame)
        assert len(df) > 0

    def test_has_required_columns(self, simple_reg_mod):
        df = simple_reg_mod.load_data()
        for col in ("BuildingAge", "PriceMan", "Area"):
            assert col in df.columns

    def test_no_station_column(self, simple_reg_mod):
        # 実 API (XIT001) に駅情報は無い。基盤も駅列を作らないことを保証する。
        df = simple_reg_mod.load_data()
        assert "TimeToNearestStation" not in df.columns


class TestSimpleRegression:
    @pytest.fixture(scope="class")
    def model(self, simple_reg_mod):
        df = simple_reg_mod.load_data()
        return simple_reg_mod.run_simple_regression(df)

    def test_building_age_coefficient_is_negative(self, model):
        assert model.params["BuildingAge"] < 0

    def test_const_is_positive(self, model):
        assert model.params["const"] > 0

    def test_r_squared_between_0_and_1(self, model):
        assert 0 < model.rsquared < 1

    def test_pvalue_is_significant(self, model):
        assert model.pvalues["BuildingAge"] < 0.05


class TestMultipleRegression:
    @pytest.fixture(scope="class")
    def model(self, multi_reg_mod):
        df = multi_reg_mod.load_data()
        return multi_reg_mod.run_multiple_regression(df)

    def test_all_pvalues_significant(self, model):
        for var in ["Area", "BuildingAge"]:
            assert model.pvalues[var] < 0.05

    def test_coefficient_signs(self, model):
        assert model.params["BuildingAge"] < 0
        assert model.params["Area"] > 0

    def test_r_squared_higher_than_simple(self, simple_reg_mod, multi_reg_mod):
        df = simple_reg_mod.load_data()
        simple_model = simple_reg_mod.run_simple_regression(df)
        multi_model = multi_reg_mod.run_multiple_regression(df)
        assert multi_model.rsquared > simple_model.rsquared


class TestResiduals:
    def test_residuals_sum_near_zero(self, multi_reg_mod):
        import statsmodels.api as sm

        df = multi_reg_mod.load_data()
        X = df[["Area", "BuildingAge"]]
        X = sm.add_constant(X)
        y = df["PriceMan"]
        model = sm.OLS(y, X).fit()
        residuals = y - model.predict(X)
        assert abs(residuals.sum()) < 1.0

    def test_predicted_plus_residual_equals_actual(self, multi_reg_mod):
        import statsmodels.api as sm

        df = multi_reg_mod.load_data()
        X = df[["Area", "BuildingAge"]]
        X = sm.add_constant(X)
        y = df["PriceMan"]
        model = sm.OLS(y, X).fit()
        predicted = model.predict(X)
        pd.testing.assert_series_equal(
            y, predicted + model.resid, check_names=False, atol=1e-6,
        )
