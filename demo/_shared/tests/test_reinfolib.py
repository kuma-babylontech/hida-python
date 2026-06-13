"""
reinfolib（XIT001 取得・正規化基盤）のテスト。

実 API のクセ（和暦の建築年・全角数字・全項目が文字列）を吸収できているかを、
実レスポンスと同じ形のデータで検証する。
"""

import pandas as pd
import pytest
import requests

import reinfolib


# ---------------------------------------------------------------------------
# 和暦 → 西暦
# ---------------------------------------------------------------------------
class TestWarekiToSeireki:
    @pytest.mark.parametrize(
        "wareki, expected",
        [
            ("令和元年", 2019),
            ("令和1年", 2019),
            ("令和3年", 2021),
            ("平成元年", 1989),
            ("平成20年", 2008),
            ("平成31年", 2019),
            ("昭和60年", 1985),
            ("昭和64年", 1989),
            ("大正元年", 1912),
            ("明治元年", 1868),
        ],
    )
    def test_converts_japanese_era(self, wareki, expected):
        assert reinfolib.wareki_to_seireki(wareki) == expected

    @pytest.mark.parametrize("seireki", ["1995年", "1995", "2010年"])
    def test_passes_through_western_year(self, seireki):
        assert reinfolib.wareki_to_seireki(seireki) == int(
            seireki.replace("年", "")
        )

    def test_fullwidth_digits_are_handled(self):
        assert reinfolib.wareki_to_seireki("平成２０年") == 2008

    @pytest.mark.parametrize("bad", ["戦前", "", "  ", None, "不明"])
    def test_unconvertible_returns_none(self, bad):
        assert reinfolib.wareki_to_seireki(bad) is None


# ---------------------------------------------------------------------------
# 全角 → 半角
# ---------------------------------------------------------------------------
class TestToHalfwidth:
    def test_converts_fullwidth_digits(self):
        assert reinfolib.to_halfwidth("2025年第４四半期") == "2025年第4四半期"

    def test_non_string_and_nan(self):
        assert reinfolib.to_halfwidth(None) == ""
        assert reinfolib.to_halfwidth(float("nan")) == ""


# ---------------------------------------------------------------------------
# normalize: 実 API 形状の生データ → 分析レディ
# ---------------------------------------------------------------------------
@pytest.fixture
def raw_records():
    """実 API レスポンスと同じ「全項目文字列・和暦・全角」の生レコード。"""
    return [
        {
            "Type": "中古マンション等",
            "Municipality": "新宿区",
            "TradePrice": "21000000",   # 文字列
            "Area": "20.5",             # 文字列
            "UnitPrice": "1024390",
            "FloorPlan": "１Ｋ",
            "BuildingYear": "平成20年",  # 和暦
            "Structure": "ＲＣ",
            "Period": "2025年第４四半期",  # 全角四半期
        },
        {
            "Type": "中古マンション等",
            "Municipality": "港区",
            "TradePrice": "33000000",
            "Area": "25",
            "UnitPrice": "1320000",
            "FloorPlan": "１Ｒ",
            "BuildingYear": "令和2年",
            "Structure": "ＳＲＣ",
            "Period": "2025年第４四半期",
        },
    ]


class TestNormalize:
    def test_numeric_columns_become_numeric(self, raw_records):
        df = reinfolib.normalize(raw_records, current_year=2025)
        assert pd.api.types.is_numeric_dtype(df["TradePrice"])
        assert pd.api.types.is_numeric_dtype(df["Area"])
        assert df.loc[0, "TradePrice"] == 21000000
        assert df.loc[0, "Area"] == 20.5

    def test_building_age_from_wareki(self, raw_records):
        df = reinfolib.normalize(raw_records, current_year=2025)
        # 平成20年 = 2008 → 築17年 / 令和2年 = 2020 → 築5年
        assert df.loc[0, "BuildingYearSeireki"] == 2008
        assert df.loc[0, "BuildingAge"] == 17
        assert df.loc[1, "BuildingAge"] == 5

    def test_period_normalized_to_halfwidth(self, raw_records):
        df = reinfolib.normalize(raw_records, current_year=2025)
        assert df.loc[0, "Period"] == "2025年第4四半期"

    def test_derived_man_columns(self, raw_records):
        df = reinfolib.normalize(raw_records, current_year=2025)
        assert df.loc[0, "PriceMan"] == 2100.0
        assert "UnitPriceMan" in df.columns

    def test_empty_input_returns_empty(self):
        df = reinfolib.normalize([])
        assert df.empty

    def test_senzen_building_year_becomes_na(self):
        records = [{"BuildingYear": "戦前", "TradePrice": "1000", "Area": "20"}]
        df = reinfolib.normalize(records, current_year=2025)
        assert pd.isna(df.loc[0, "BuildingAge"])


# ---------------------------------------------------------------------------
# fetch_transactions: 本番 API 呼び出し（requests をスタブ）
# ---------------------------------------------------------------------------
class TestFetchTransactions:
    def test_raises_without_key(self, monkeypatch):
        monkeypatch.delenv("REINFOLIB_API_KEY", raising=False)
        with pytest.raises(RuntimeError):
            reinfolib.fetch_transactions(2025, 1)

    def test_calls_api_with_correct_params(self, monkeypatch):
        captured = {}

        class _Resp:
            status_code = 200

            def raise_for_status(self):
                pass

            def json(self):
                return {"status": "OK", "data": [{"TradePrice": "100"}]}

        def fake_get(url, **kwargs):
            captured["url"] = url
            captured.update(kwargs.get("params", {}))
            captured["headers"] = kwargs.get("headers", {})
            return _Resp()

        monkeypatch.setattr(requests, "get", fake_get)
        records = reinfolib.fetch_transactions(2025, 3, area="13", api_key="KEY")

        assert captured["url"] == reinfolib.API_URL
        assert captured["year"] == "2025"
        assert captured["quarter"] == "3"
        assert captured["area"] == "13"
        assert captured["headers"]["Ocp-Apim-Subscription-Key"] == "KEY"
        assert records == [{"TradePrice": "100"}]


# ---------------------------------------------------------------------------
# load_dataframe: オフラインサンプル経由のエンドツーエンド
# ---------------------------------------------------------------------------
class TestLoadDataframeOffline:
    @pytest.fixture(scope="class")
    def df(self):
        # 鍵が無い環境を保証してオフラインサンプルを使わせる。
        import os

        saved = os.environ.pop("REINFOLIB_API_KEY", None)
        try:
            yield reinfolib.load_dataframe(current_year=2025)
        finally:
            if saved is not None:
                os.environ["REINFOLIB_API_KEY"] = saved

    def test_has_rows(self, df):
        assert len(df) > 0

    def test_analysis_ready_columns(self, df):
        for col in ("PriceMan", "Area", "BuildingAge"):
            assert col in df.columns

    def test_no_station_fields(self, df):
        # 実 API に無い駅情報がサンプルにも無いこと（忠実性の担保）。
        assert "NearestStation" not in df.columns
        assert "TimeToNearestStation" not in df.columns

    def test_building_age_is_clean_int(self, df):
        assert pd.api.types.is_integer_dtype(df["BuildingAge"])
        assert df["BuildingAge"].notna().all()
        assert (df["BuildingAge"] >= 0).all()

    def test_only_oneroom(self, df):
        assert df["FloorPlan"].str.contains("１Ｒ|１Ｋ|1R|1K").all()
