"""
不動産情報ライブラリ XIT001 API の**実レスポンスに忠実な**サンプルを生成する。

鍵が無くてもデモ・テストを動かせるようにするためのオフラインデータ。
旧サンプル（demo/2026-04-real-estate-eda/data/tokyo_mansion.csv）と違い、
実 API のクセを忠実に再現している:

  - 建築年は **和暦**（"平成20年"）
  - 取引時期の四半期は **全角数字**（"2025年第４四半期"）
  - 構造・間取りは **全角**（"ＲＣ" / "１Ｋ"）
  - 数値も含め **全項目を文字列** として書き出す
  - 実 API に無い最寄駅・駅徒歩・路線フィールドは **含めない**

これにより reinfolib.normalize() の和暦変換・全角処理・型変換が実データと同じ条件で
検証される。出力は ``sample_xit001.csv``。
"""

import csv
import random
from pathlib import Path

random.seed(42)

# 東京23区の代表的なエリア（ワンルーム投資で人気）と市区町村コード。
AREAS = [
    ("13104", "新宿区", "西新宿"),
    ("13104", "新宿区", "高田馬場"),
    ("13113", "渋谷区", "恵比寿"),
    ("13113", "渋谷区", "渋谷"),
    ("13116", "豊島区", "南池袋"),
    ("13116", "豊島区", "大塚"),
    ("13114", "中野区", "中野"),
    ("13115", "杉並区", "荻窪"),
    ("13115", "杉並区", "高円寺"),
    ("13119", "板橋区", "板橋"),
    ("13117", "北区", "赤羽"),
    ("13106", "台東区", "上野"),
    ("13107", "墨田区", "錦糸町"),
    ("13108", "江東区", "門前仲町"),
    ("13109", "品川区", "東五反田"),
    ("13109", "品川区", "大井"),
    ("13111", "大田区", "蒲田"),
    ("13105", "文京区", "小石川"),
    ("13102", "中央区", "日本橋小網町"),
    ("13103", "港区", "三田"),
]

# エリアごとの価格帯（万円/㎡）の基準値。
AREA_PRICE_BASE = {
    "港区": 130, "渋谷区": 120, "中央区": 115, "新宿区": 105,
    "文京区": 100, "品川区": 95, "豊島区": 85, "台東区": 85,
    "中野区": 80, "北区": 70, "墨田区": 75, "江東区": 78,
    "杉並区": 78, "板橋区": 65, "大田区": 68,
}

# 取引時期: 直近8四半期。四半期だけ全角にして実 API を再現する。
_ZEN = str.maketrans("0123456789", "０１２３４５６７８９")
PERIODS = [f"{y}年第{str(q).translate(_ZEN)}四半期"
           for y in (2024, 2025) for q in (1, 2, 3, 4)]

STRUCTURES = ["ＳＲＣ", "ＲＣ", "鉄骨造", "軽量鉄骨造"]


def seireki_to_wareki(year: int) -> str:
    """西暦 → 和暦（実 API と同じ "平成20年" 形式。元年も "平成1年" 表記）。"""
    if year >= 2019:
        return f"令和{year - 2018}年"
    if year >= 1989:
        return f"平成{year - 1988}年"
    if year >= 1926:
        return f"昭和{year - 1925}年"
    return f"大正{year - 1911}年"


def generate_record() -> dict:
    code, municipality, district = random.choice(AREAS)
    area = round(random.uniform(16, 30), 2)            # ワンルーム: 16〜30㎡
    building_year = random.randint(1985, 2020)
    age = 2025 - building_year

    # 価格モデル: エリア基準 × 面積 − 築年数減価 + ノイズ。
    base = AREA_PRICE_BASE[municipality]
    price_per_sqm = base - age * 1.2 + random.gauss(0, 10)
    price_per_sqm = max(price_per_sqm, 30)
    trade_price = int(price_per_sqm * area * 10000)

    # 実 API に合わせ、全項目を文字列で返す（最寄駅・駅徒歩は含めない）。
    return {
        "Type": "中古マンション等",
        "MunicipalityCode": code,
        "Prefecture": "東京都",
        "Municipality": municipality,
        "DistrictName": district,
        "TradePrice": str(trade_price),
        "Area": str(area),
        "UnitPrice": str(int(price_per_sqm * 10000)),
        "FloorPlan": "１Ｋ" if random.random() < 0.6 else "１Ｒ",
        "BuildingYear": seireki_to_wareki(building_year),
        "Structure": random.choice(STRUCTURES),
        "Use": "住宅",
        "CityPlanning": "商業地域" if random.random() < 0.4 else "準工業地域",
        "Period": random.choice(PERIODS),
        "Renovation": "改装済" if random.random() < 0.3 else "未改装",
    }


def main() -> None:
    records = [generate_record() for _ in range(500)]
    output_path = Path(__file__).resolve().parent / "sample_xit001.csv"

    fieldnames = list(records[0].keys())
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)

    print(f"Generated {len(records)} records → {output_path}")


if __name__ == "__main__":
    main()
