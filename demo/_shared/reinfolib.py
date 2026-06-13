"""
不動産情報ライブラリ XIT001 API の取得・正規化基盤（Part1〜3 共通モジュール）。

国土交通省「不動産情報ライブラリ」の取引価格情報取得 API (XIT001) から
データを取得し、**そのまま pandas で分析できる形** に整える層。

なぜこの層が要るのか
--------------------
実 API のレスポンスにはクセがあり、素朴に DataFrame 化すると分析コードが壊れる。

1. **全項目が文字列**で返る（``TradePrice="98000000"`` など）。
   そのまま ``df["TradePrice"] / 10000`` すると文字列演算で失敗する。
2. **建築年が和暦**（``BuildingYear="平成20年"``）。
   ``str.replace("年","").astype(int)`` は ``平成20`` で即クラッシュする。
3. **全角数字**が混じる（``Period="2025年第４四半期"`` / ``Structure="ＲＣ"``）。

このモジュールがこれらを吸収し、``BuildingAge`` / ``PriceMan`` などの派生列まで
付けた「分析レディな DataFrame」を返す。

実 API に最寄駅は無い
---------------------
XIT001 の出力に ``NearestStation`` / ``TimeToNearestStation`` は **存在しない**
（公式マニュアルの出力項目に駅情報は含まれない）。駅徒歩を使った分析はできないため、
面積・築年数・用途地域・構造などの実在する項目で代替する。

使い方
------
>>> import reinfolib
>>> df = reinfolib.load_dataframe()        # 分析レディな DataFrame
>>> df[["PriceMan", "Area", "BuildingAge"]].describe()

環境変数 ``REINFOLIB_API_KEY`` があれば本番 API を叩き、無ければ実 API レスポンスに
忠実なオフラインサンプル（``sample_xit001.csv``）で代替する。
"""

from __future__ import annotations

import os
import re
from datetime import datetime
from pathlib import Path
from typing import Iterable, Optional

import pandas as pd
import requests

API_URL = "https://www.reinfolib.mlit.go.jp/ex-api/external/XIT001"

#: 実 API は全項目を文字列で返すため、数値として扱う列を明示する。
NUMERIC_COLUMNS = (
    "TradePrice",
    "Area",
    "UnitPrice",
    "PricePerUnit",
    "TotalFloorArea",
    "Frontage",
    "Breadth",
    "CoverageRatio",
    "FloorAreaRatio",
)

#: 鍵が無いときに使う、実 API レスポンスに忠実なオフラインサンプル（生データ）。
SAMPLE_CSV = Path(__file__).resolve().parent / "sample_xit001.csv"

#: 元号 → 西暦の開始年（元年 = 開始年）。
_ERA_START = {"明治": 1868, "大正": 1912, "昭和": 1926, "平成": 1989, "令和": 2019}

_ZEN_TO_HAN = str.maketrans("０１２３４５６７８９", "0123456789")

_SEIREKI_RE = re.compile(r"^(\d{3,4})年?$")
_WAREKI_RE = re.compile(r"^(明治|大正|昭和|平成|令和)(元|\d+)年?$")


def to_halfwidth(value) -> str:
    """全角数字を含む文字列を半角化する。非文字列は文字列化して返す。"""
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return ""
    return str(value).translate(_ZEN_TO_HAN)


def wareki_to_seireki(value) -> Optional[int]:
    """
    建築年を西暦（int）に変換する。

    ``"平成20年"`` → ``2008`` / ``"令和元年"`` → ``2019`` のように和暦を西暦へ。
    既に西暦（``"1995年"`` / ``"1995"``）ならそのまま数値化する。
    ``"戦前"`` や空・不明値は ``None`` を返す（呼び出し側で除外できる）。
    """
    s = to_halfwidth(value).strip()
    if not s:
        return None

    m = _SEIREKI_RE.match(s)
    if m:
        return int(m.group(1))

    m = _WAREKI_RE.match(s)
    if m:
        era, year_part = m.group(1), m.group(2)
        n = 1 if year_part == "元" else int(year_part)
        return _ERA_START[era] + n - 1

    return None  # "戦前" など変換不能な値


def get_api_key() -> str:
    return os.environ.get("REINFOLIB_API_KEY", "")


def is_live() -> bool:
    """本番 API を使うか（＝鍵が設定されているか）。"""
    return bool(get_api_key())


def fetch_transactions(
    year: int,
    quarter: int,
    area: str = "13",
    *,
    api_key: Optional[str] = None,
    timeout: int = 30,
) -> list[dict]:
    """
    XIT001 から取引価格情報を取得し、生レコード（dict のリスト）を返す。

    Parameters
    ----------
    year : int
        取引年（2005〜）。
    quarter : int
        四半期（1〜4）。
    area : str
        都道府県コード（東京都 = ``"13"``）。
    """
    api_key = api_key or get_api_key()
    if not api_key:
        raise RuntimeError(
            "REINFOLIB_API_KEY が未設定です。本番 API を呼ぶには鍵を設定してください。"
        )

    resp = requests.get(
        API_URL,
        headers={"Ocp-Apim-Subscription-Key": api_key},
        params={
            "year": str(year),
            "quarter": str(quarter),
            "area": area,
            "language": "ja",
        },
        timeout=timeout,
    )
    resp.raise_for_status()
    payload = resp.json()
    return payload.get("data", [])


def _load_sample_records() -> list[dict]:
    """オフラインサンプルを実 API と同じ「全項目文字列」の dict リストで返す。"""
    return pd.read_csv(SAMPLE_CSV, dtype=str).fillna("").to_dict("records")


def normalize(records, *, current_year: Optional[int] = None) -> pd.DataFrame:
    """
    実 API の生レコード（文字列・和暦・全角）を分析レディな DataFrame に整える。

    付与する派生列:
      - ``BuildingYearSeireki`` : 建築年（西暦・Int64）
      - ``BuildingAge``         : 築年数（current_year − 西暦）
      - ``PriceMan``            : 取引価格（万円）
      - ``UnitPriceMan``        : 平米単価（万円）
    """
    if current_year is None:
        current_year = datetime.now().year

    df = records.copy() if isinstance(records, pd.DataFrame) else pd.DataFrame(records)
    if df.empty:
        return df

    # 1. 数値列を文字列 → 数値へ（全角も吸収）。変換不能は NaN。
    for col in NUMERIC_COLUMNS:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col].map(to_halfwidth), errors="coerce")

    # 2. 建築年: 和暦 → 西暦、そこから築年数。
    if "BuildingYear" in df.columns:
        seireki = df["BuildingYear"].map(wareki_to_seireki)
        df["BuildingYearSeireki"] = seireki.astype("Int64")
        df["BuildingAge"] = (current_year - df["BuildingYearSeireki"]).astype("Int64")

    # 3. 取引時期: 全角 → 半角に統一。
    if "Period" in df.columns:
        df["Period"] = df["Period"].map(to_halfwidth)

    # 4. 万円スケールの派生列。
    if "TradePrice" in df.columns:
        df["PriceMan"] = df["TradePrice"] / 10000
    if "UnitPrice" in df.columns:
        df["UnitPriceMan"] = df["UnitPrice"] / 10000

    return df


def load_dataframe(
    years: Iterable[int] = (2025,),
    quarters: Iterable[int] = (1, 2, 3, 4),
    area: str = "13",
    *,
    oneroom_only: bool = True,
    dropna_subset: Iterable[str] = ("TradePrice", "Area", "BuildingAge"),
    current_year: Optional[int] = None,
) -> pd.DataFrame:
    """
    分析レディな DataFrame を返す高レベル入口。

    鍵があれば本番 API（指定した年・四半期を全取得）、無ければオフラインサンプル。
    正規化したうえで、ワンルーム・1K に絞り込み、分析に必須の列が欠損する行を落とす。
    """
    if is_live():
        frames = [
            pd.DataFrame(fetch_transactions(y, q, area))
            for y in years
            for q in quarters
        ]
        non_empty = [f for f in frames if not f.empty]
        raw = pd.concat(non_empty, ignore_index=True) if non_empty else pd.DataFrame()
    else:
        raw = pd.DataFrame(_load_sample_records())

    df = normalize(raw, current_year=current_year)
    if df.empty:
        return df

    if oneroom_only and "FloorPlan" in df.columns:
        mask = df["FloorPlan"].astype(str).str.contains("１Ｒ|１Ｋ|1R|1K", na=False)
        df = df[mask]

    subset = [c for c in dropna_subset if c in df.columns]
    if subset:
        df = df.dropna(subset=subset)

    # 欠損を落とした後は築年数を素の int にして下流（statsmodels 等）で扱いやすくする。
    if "BuildingAge" in df.columns:
        df["BuildingAge"] = df["BuildingAge"].astype(int)
    if "BuildingYearSeireki" in df.columns:
        df["BuildingYearSeireki"] = df["BuildingYearSeireki"].astype(int)

    return df.reset_index(drop=True)


def main() -> None:
    """CLI: 取得結果を分析レディな CSV に保存する。"""
    mode = "本番 API" if is_live() else "オフラインサンプル"
    print(f"データソース: {mode}")

    df = load_dataframe()
    print(f"取得 {len(df)} 件（ワンルーム・1K）")

    out_dir = Path(__file__).resolve().parent / "output"
    out_dir.mkdir(exist_ok=True)
    out_path = out_dir / "tokyo_mansion_analysis_ready.csv"
    df.to_csv(out_path, index=False)
    print(f"保存しました → {out_path}")


if __name__ == "__main__":
    main()
