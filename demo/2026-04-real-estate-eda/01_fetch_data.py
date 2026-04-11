"""
不動産情報ライブラリ API からデータを取得する（モック版）。

本来の API キー申請: https://www.reinfolib.mlit.go.jp/api/request/ （無料・約5営業日）
エンドポイント: https://www.reinfolib.mlit.go.jp/ex-api/external/XIT001

※ 発表時点で API キーが発行待ちのため、`unittest.mock` で `requests.get`
   を差し替えてデモを行う。キーが発行されれば `USE_MOCK = False` にする
   だけで同じコードが本番 API に通る。
"""

import csv
import os
from pathlib import Path
from unittest.mock import patch, MagicMock

import pandas as pd
import requests

API_URL = "https://www.reinfolib.mlit.go.jp/ex-api/external/XIT001"
API_KEY = os.environ.get("REINFOLIB_API_KEY", "")
USE_MOCK = not API_KEY  # キー未設定ならモックを使う

SAMPLE_CSV = Path(__file__).parent / "data" / "tokyo_mansion.csv"


def _load_sample_records() -> list[dict]:
    """サンプル CSV を API レスポンス形式の dict リストに変換する。"""
    with open(SAMPLE_CSV, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def _mock_api_response(*args, **kwargs):
    """
    requests.get の代わりに呼ばれるモック関数。
    実際の reinfolib XIT001 レスポンス仕様 `{"status": "OK", "data": [...]}`
    に合わせて返す。params の year/quarter でフィルタもする。
    """
    params = kwargs.get("params", {})
    year = params.get("year")
    quarter = params.get("quarter")
    target_period = f"{year}年第{quarter}四半期"

    records = _load_sample_records()
    filtered = [r for r in records if r.get("Period") == target_period]

    mock_resp = MagicMock(spec=requests.Response)
    mock_resp.status_code = 200
    mock_resp.json.return_value = {"status": "OK", "data": filtered}
    mock_resp.raise_for_status.return_value = None
    return mock_resp


def fetch_transactions(year: int, quarter: int, area: str = "13") -> pd.DataFrame:
    """
    不動産取引価格情報を取得する。

    Parameters
    ----------
    year : int
        取引年（2005〜）
    quarter : int
        四半期（1〜4）
    area : str
        都道府県コード（東京都 = "13"）
    """
    resp = requests.get(
        API_URL,
        headers={"Ocp-Apim-Subscription-Key": API_KEY or "MOCK_KEY"},
        params={
            "year": str(year),
            "quarter": str(quarter),
            "area": area,
            "language": "ja",
        },
        timeout=30,
    )
    resp.raise_for_status()
    payload = resp.json()
    return pd.DataFrame(payload.get("data", []))


def main():
    if USE_MOCK:
        print("⚠ API キー未設定 — モックモードで実行します")
        print(f"  サンプルソース: {SAMPLE_CSV}")
        print("  （本物のキーを使う場合は環境変数 REINFOLIB_API_KEY を設定）")
        print()
        ctx = patch("requests.get", side_effect=_mock_api_response)
    else:
        print("✓ API キーを検出 — 本番 API を呼び出します")
        from contextlib import nullcontext
        ctx = nullcontext()

    with ctx:
        frames = []
        for q in range(1, 5):
            print(f"Fetching 2025 Q{q}...")
            df = fetch_transactions(2025, q)
            print(f"  → {len(df)} records")
            if not df.empty:
                frames.append(df)

    if not frames:
        print("データを取得できませんでした。")
        return

    df_all = pd.concat(frames, ignore_index=True)
    # ワンルーム・1K に絞り込み
    mask = df_all["FloorPlan"].str.contains("１Ｒ|１Ｋ|1R|1K", na=False)
    df_filtered = df_all[mask].copy()

    out_path = SAMPLE_CSV.parent / "tokyo_mansion_fetched.csv"
    df_filtered.to_csv(out_path, index=False)
    print(f"\nSaved {len(df_filtered)} records → {out_path}")


if __name__ == "__main__":
    main()
