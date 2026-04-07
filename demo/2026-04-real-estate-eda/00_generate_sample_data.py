"""
不動産情報ライブラリ API のレスポンスに準拠したサンプルデータを生成する。

API キー未取得でもデモを実行できるように、
東京23区の中古ワンルームマンション取引データを模擬生成する。
実際の API レスポンスと同じカラム名を使用。
"""

import csv
import random
from pathlib import Path

random.seed(42)

# 東京23区の代表的なエリアと駅（ワンルーム投資で人気のエリア）
AREAS = [
    ("新宿区", "新宿", "JR山手線"),
    ("新宿区", "高田馬場", "JR山手線"),
    ("渋谷区", "渋谷", "JR山手線"),
    ("渋谷区", "恵比寿", "JR山手線"),
    ("豊島区", "池袋", "JR山手線"),
    ("豊島区", "大塚", "JR山手線"),
    ("中野区", "中野", "JR中央線"),
    ("杉並区", "荻窪", "JR中央線"),
    ("杉並区", "高円寺", "JR中央線"),
    ("板橋区", "板橋", "JR埼京線"),
    ("北区", "赤羽", "JR京浜東北線"),
    ("台東区", "上野", "JR山手線"),
    ("墨田区", "錦糸町", "JR総武線"),
    ("江東区", "門前仲町", "東京メトロ東西線"),
    ("品川区", "五反田", "JR山手線"),
    ("品川区", "大井町", "JR京浜東北線"),
    ("大田区", "蒲田", "JR京浜東北線"),
    ("文京区", "茗荷谷", "東京メトロ丸ノ内線"),
    ("中央区", "人形町", "東京メトロ日比谷線"),
    ("港区", "田町", "JR山手線"),
]

# エリアごとの価格帯（万円/㎡）の基準値
AREA_PRICE_BASE = {
    "港区": 130, "渋谷区": 120, "中央区": 115, "新宿区": 105,
    "文京区": 100, "品川区": 95, "豊島区": 85, "台東区": 85,
    "中野区": 80, "北区": 70, "墨田区": 75, "江東区": 78,
    "杉並区": 78, "板橋区": 65, "大田区": 68,
}

PERIODS = [
    "2024年第1四半期", "2024年第2四半期",
    "2024年第3四半期", "2024年第4四半期",
    "2025年第1四半期", "2025年第2四半期",
    "2025年第3四半期", "2025年第4四半期",
]

STRUCTURES = ["SRC", "RC", "鉄骨造", "軽量鉄骨造"]


def generate_record():
    municipality, station, line = random.choice(AREAS)
    area = round(random.uniform(16, 30), 2)  # ワンルーム: 16〜30㎡
    building_year = random.randint(1985, 2020)
    age = 2025 - building_year
    time_to_station = random.randint(1, 15)

    # 価格モデル: エリア基準 × 面積 - 築年数減価 - 駅距離減価 + ノイズ
    base = AREA_PRICE_BASE[municipality]
    price_per_sqm = (
        base
        - age * 1.2                          # 築1年あたり約1.2万円/㎡ 減価
        - time_to_station * 1.5              # 徒歩1分あたり約1.5万円/㎡ 減価
        + random.gauss(0, 10)                # ノイズ
    )
    price_per_sqm = max(price_per_sqm, 30)   # 下限
    trade_price = int(price_per_sqm * area * 10000)  # 円に変換

    return {
        "Type": "中古マンション等",
        "TradePrice": trade_price,
        "UnitPrice": int(price_per_sqm * 10000),
        "Area": area,
        "Municipality": municipality,
        "NearestStation": station,
        "TimeToNearestStation": time_to_station,
        "FloorPlan": "１Ｋ" if random.random() < 0.6 else "１Ｒ",
        "BuildingYear": f"{building_year}年",
        "Structure": random.choice(STRUCTURES),
        "Prefecture": "東京都",
        "Period": random.choice(PERIODS),
        "CityPlanning": "商業地域" if random.random() < 0.4 else "準工業地域",
        "Railway": line,
    }


def main():
    records = [generate_record() for _ in range(500)]
    output_path = Path(__file__).parent / "data" / "tokyo_mansion.csv"
    output_path.parent.mkdir(exist_ok=True)

    fieldnames = list(records[0].keys())
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)

    print(f"Generated {len(records)} records → {output_path}")


if __name__ == "__main__":
    main()
