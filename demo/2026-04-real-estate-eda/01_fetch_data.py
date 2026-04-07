"""
不動産情報ライブラリ API からデータを取得する。

API キー: https://www.reinfolib.mlit.go.jp/api/request/ で無料申請（約5営業日）
エンドポイント: https://www.reinfolib.mlit.go.jp/ex-api/external/XIT001
"""

import os

import requests
import pandas as pd

API_URL = "https://www.reinfolib.mlit.go.jp/ex-api/external/XIT001"
API_KEY = os.environ.get("REINFOLIB_API_KEY", "")


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
    if not API_KEY:
        print("⚠ API キーが設定されていません")
        print("  環境変数 REINFOLIB_API_KEY を設定してください")
        print("  API キー申請: https://www.reinfolib.mlit.go.jp/api/request/")
        print()
        print("→ 代わりにサンプルデータ (data/tokyo_mansion.csv) を使用してください")
        return pd.DataFrame()

    resp = requests.get(
        API_URL,
        headers={"Ocp-Apim-Subscription-Key": API_KEY},
        params={
            "year": str(year),
            "quarter": str(quarter),
            "area": area,
            "language": "ja",
        },
        timeout=30,
    )
    resp.raise_for_status()
    data = resp.json()
    return pd.DataFrame(data)


def main():
    # 2025年の4四半期分を取得
    frames = []
    for q in range(1, 5):
        print(f"Fetching 2025 Q{q}...")
        df = fetch_transactions(2025, q)
        if not df.empty:
            frames.append(df)

    if frames:
        df_all = pd.concat(frames, ignore_index=True)
        # ワンルーム・1K に絞り込み
        mask = df_all["FloorPlan"].str.contains("１Ｒ|１Ｋ|1R|1K", na=False)
        df_filtered = df_all[mask].copy()
        df_filtered.to_csv("data/tokyo_mansion.csv", index=False)
        print(f"Saved {len(df_filtered)} records")
    else:
        print("データを取得できませんでした。サンプルデータを使用してください。")


if __name__ == "__main__":
    main()
