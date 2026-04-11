"""
01_fetch_data.py のテスト。

- モック関数が reinfolib XIT001 と同じレスポンス形状を返すこと
- params の year/quarter に応じてフィルタリングされること
- fetch_transactions が monkeypatch された requests.get を経由して DataFrame を返すこと
"""

import pandas as pd
import pytest
import requests


class TestMockApiResponse:
    def test_returns_status_ok_and_data_key(self, fetch_data_mod):
        resp = fetch_data_mod._mock_api_response(
            params={"year": "2025", "quarter": "1", "area": "13"}
        )
        payload = resp.json()
        assert payload["status"] == "OK"
        assert "data" in payload
        assert isinstance(payload["data"], list)

    def test_response_has_http_like_interface(self, fetch_data_mod):
        resp = fetch_data_mod._mock_api_response(
            params={"year": "2025", "quarter": "1"}
        )
        assert resp.status_code == 200
        resp.raise_for_status()  # 例外が飛ばなければOK

    @pytest.mark.parametrize("quarter", ["1", "2", "3", "4"])
    def test_filters_by_period(self, fetch_data_mod, quarter):
        resp = fetch_data_mod._mock_api_response(
            params={"year": "2025", "quarter": quarter}
        )
        records = resp.json()["data"]
        expected_period = f"2025年第{quarter}四半期"
        assert all(r["Period"] == expected_period for r in records)

    def test_unknown_period_returns_empty(self, fetch_data_mod):
        resp = fetch_data_mod._mock_api_response(
            params={"year": "1999", "quarter": "1"}
        )
        assert resp.json()["data"] == []

    def test_records_have_expected_schema(self, fetch_data_mod):
        resp = fetch_data_mod._mock_api_response(
            params={"year": "2025", "quarter": "1"}
        )
        records = resp.json()["data"]
        assert len(records) > 0
        required = {
            "TradePrice", "Area", "BuildingYear", "Municipality",
            "NearestStation", "TimeToNearestStation", "Period", "FloorPlan",
        }
        assert required.issubset(records[0].keys())


class TestFetchTransactions:
    def test_returns_dataframe_via_monkeypatched_requests(
        self, fetch_data_mod, monkeypatch
    ):
        monkeypatch.setattr(
            requests, "get", fetch_data_mod._mock_api_response
        )
        df = fetch_data_mod.fetch_transactions(2025, 1)
        assert isinstance(df, pd.DataFrame)
        assert len(df) > 0
        assert "TradePrice" in df.columns

    def test_passes_correct_params(self, fetch_data_mod, monkeypatch):
        captured = {}

        def spy(*args, **kwargs):
            captured.update(kwargs.get("params", {}))
            return fetch_data_mod._mock_api_response(*args, **kwargs)

        monkeypatch.setattr(requests, "get", spy)
        fetch_data_mod.fetch_transactions(2025, 3, area="13")
        assert captured["year"] == "2025"
        assert captured["quarter"] == "3"
        assert captured["area"] == "13"

    def test_empty_when_no_matching_period(self, fetch_data_mod, monkeypatch):
        monkeypatch.setattr(requests, "get", fetch_data_mod._mock_api_response)
        df = fetch_data_mod.fetch_transactions(1999, 1)
        assert isinstance(df, pd.DataFrame)
        assert df.empty
