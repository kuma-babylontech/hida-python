---
title: "2025年 Python動向振り返り"
date: 2025-12-19
description: "飛騨高山Pythonの会#71 発表資料。TIOBEランキング、Python 3.14新機能、Rust製ツールの台頭など2025年のPython動向を総まとめ。"
tags:
  - Python
  - 振り返り
  - 2025年
author: ""
---

# 2025年 Python動向振り返り

飛騨高山Pythonの会#71 発表資料

2025/12/19

---

## 目次

1. 人気度・ランキング
2. バージョン動向とEOL
3. Python 3.14 主要新機能
4. 開発ツールの進化
5. エコシステムの変化
6. 今後の展望

---

## 1. 人気度・ランキング

---

### TIOBEインデックス 歴史的最高位を記録

- **2025年5月：25.35%** を記録（史上最高）
- 2位のC++に **15ポイント以上** の差をつける
- 2001年のJava（26.49%）以来の高水準
  - 当時は20言語のみ → 現在は282言語を追跡

> 「他の言語が存在する唯一の理由は、Pythonの低パフォーマンスと
> インタプリタ実行による予期せぬランタイムエラーの存在」
> — TIOBE CEO Paul Jansen

---

### 2025年12月 TIOBEトップ10

| 順位 | 言語 | 備考 |
|------|------|------|
| 1 | **Python** | 圧倒的首位を維持 |
| 2 | C | C23採用で上昇 |
| 3 | C++ | C++26開発中 |
| 4 | Java | Java 25リリース |
| 5 | C# | 急上昇中（年間最優秀候補） |
| 6 | JavaScript | |
| 7 | Go | |
| 8 | SQL | 上昇 |
| 9 | Visual Basic | |
| 10 | **R** | 新規ランクイン |

※ Delphi/Object Pascalがトップ10から脱落

---

### Python バージョン別利用状況

**JetBrains調査より**

- Python 3.11：**48%**（最多）
- Python 3.9 以前：約 **8-10%** が本番運用中

**バージョンアップしない理由**

- 依存ライブラリの互換性問題
- 既存システムの変更コスト
- テスト工数の確保が困難

---

## 2. バージョン動向とEOL

---

### 2025年 主要リリースタイムライン

```
2025年
├── 10月7日   Python 3.14.0 正式リリース
├── 10月14日  Python 3.15.0a1 アルファ開始
├── 10月31日  Python 3.9 EOL
├── 11月19日  Python 3.15.0a2
├── 12月3日   Django 6.0 リリース
└── 12月16日  Python 3.15.0a3
```

---

### Python 3.9 EOL（2025年10月31日）

**影響**

- セキュリティパッチの提供終了
- バグ修正の提供終了
- 主要ライブラリのサポート終了開始

**EOL後のリスク**

- 新規CVEへの対応なし
- Cloud Run, Lambda等でランタイム非推奨化
- パッケージメンテナのテスト対象外に

**推奨アクション**

→ Python 3.13 または 3.14 へのアップグレード

---

### アップグレードによるパフォーマンス向上

**Python 3.11 → 3.13 への移行効果**

| 指標 | 改善幅 |
|------|--------|
| 実行速度 | **約11%高速化** |
| メモリ使用量 | **10-15%削減** |

**コード変更不要で恩恵を受けられる**

- 適応型インタプリタの最適化
- ゼロコスト例外処理
- 起動時間の短縮

---

### 現在サポート中のバージョン

| バージョン | 初回リリース | サポート終了 | 状態 |
|------------|--------------|--------------|------|
| 3.14 | 2025年10月 | 2030年10月 | **最新** |
| 3.13 | 2024年10月 | 2029年10月 | バグ修正中 |
| 3.12 | 2023年10月 | 2028年10月 | バグ修正中 |
| 3.11 | 2022年10月 | 2027年10月 | セキュリティのみ |
| 3.10 | 2021年10月 | 2026年10月 | セキュリティのみ |

---

## 3. Python 3.14 主要新機能

---

### Python 3.14 ハイライト

**PEP 779：Free-threaded Python（No-GIL）公式サポート**

**PEP 750：テンプレート文字列（t-strings）**

**PEP 734：標準ライブラリでの複数インタプリタ**

**PEP 649：アノテーションの遅延評価**

**PEP 784：Zstandard圧縮モジュール**

**JITコンパイラ（実験的）**

---

### t-strings（テンプレート文字列）

**f-stringの進化系**

```python
# f-string（従来）
name = "Alice"
f"Hello, {name}!"  # → "Hello, Alice!"

# t-string（Python 3.14）
name = "Alice"
t"Hello, {name}!"  # → Template オブジェクト
```

**特徴**

- 文字列と補間値に個別アクセス可能
- 出力前にカスタム処理を挿入
- SQLインジェクション/XSS対策に有効

---

### t-strings 活用例

```python
from string.templatelib import Template

user_input = "<script>alert('XSS')</script>"

# HTMLエスケープ処理を自動適用
template = t"<p>{user_input}</p>"

def html(t: Template) -> str:
    # 補間値を安全にエスケープして結合
    result = ""
    for part in t:
        if isinstance(part, str):
            result += part
        else:
            result += escape_html(part.value)
    return result

safe = html(template)
# → "<p>&lt;script&gt;alert('XSS')&lt;/script&gt;</p>"
```

---

### Free-threaded Python（No-GIL）

**GIL（Global Interpreter Lock）とは？**

- スレッド間の同時実行を制限するロック
- マルチコアCPUの性能を活かしきれない原因

**Python 3.14での変化**

- **PEP 779** により公式サポートに昇格
- 実験的 → サポート対象（ただし任意有効化）
- 真のマルチスレッド並列実行が可能に

**シングルスレッド性能への影響**

- 約 5-10% の性能低下（プラットフォーム依存）

---

### Free-threaded Python 活用イメージ

```python
import threading
import queue

def process_data(sensor_id, data_queue):
    """センサーデータを並列処理"""
    while not data_queue.empty():
        data = data_queue.get()
        # CPU集約型の処理
        analyze(data)

# Free-threaded Pythonでは
# 全スレッドが真に並列実行される
threads = []
for i in range(10):
    t = threading.Thread(
        target=process_data,
        args=(i, data_queue)
    )
    threads.append(t)
    t.start()
```

---

### concurrent.interpreters モジュール

**複数インタプリタを標準ライブラリから利用可能に**

```python
import concurrent.interpreters as interpreters

# 独立したインタプリタを作成
interp = interpreters.create()

# 別インタプリタでコード実行
interpreters.run_string(interp, """
import heavy_computation
result = heavy_computation.run()
""")
```

**メリット**

- プロセス分離より軽量
- GILを共有しない真の並列実行
- CSPやActorモデルの実装が容易に

---

### その他の注目機能

**Zstandard圧縮（PEP 784）**

```python
import compression.zstd as zstd

# 高速・高圧縮率のZstandard
compressed = zstd.compress(data)
```

**改善されたREPL**

- シンタックスハイライト
- マルチライン編集の強化
- カラー表示（unittest, argparse等も対応）

**リモートデバッガ**

- `pdb` でプロセスIDを指定してアタッチ可能

---

## 4. 開発ツールの進化

---

### uv - 次世代パッケージマネージャー

**Astral社（Ruff開発元）による Rust 製ツール**

```bash
# インストール
curl -LsSf https://astral.sh/uv/install.sh | sh

# プロジェクト初期化からパッケージ追加まで
uv init myproject
cd myproject
uv add requests flask

# 実行
uv run python app.py
```

**置き換え対象**

pip, pip-tools, pipx, poetry, pyenv, virtualenv, twine...

---

### uv のパフォーマンス

**速度比較（pip対比）**

| シナリオ | 速度向上 |
|----------|----------|
| キャッシュなし | **8-10倍** |
| キャッシュあり | **80-115倍** |

**主な機能**

- プロジェクト管理（`uv init`, `uv add`, `uv lock`）
- Python自体のインストール（`uv python install`）
- ツール実行（`uvx ruff check`）
- スクリプト実行（インラインメタデータ対応）
- ワークスペースサポート

---

### Rust製Pythonツールの台頭

**2025年は「Rust製ツールが標準になった年」**

| ツール | 用途 | 開発元 |
|--------|------|--------|
| **Ruff** | Linter/Formatter | Astral |
| **uv** | パッケージマネージャ | Astral |
| **ty** | 型チェッカー | Astral |
| **Pyrefly** | 型チェッカー | Meta |

**Python Language Summit 2025**

> 「ネイティブコードの1/4〜1/3がRust製に」

---

### Ruff 最新動向

**バージョン 0.12（2025年6月）**

- 複数Pythonバージョンのサポート強化
- f-stringフォーマット改善
- Python 3.14 t-string対応

**特徴**

- Flake8の **1000倍** 高速（誇張ではない）
- Black互換フォーマッタ内蔵
- 500以上のルールをサポート

```bash
# uvと組み合わせて即座に実行
uvx ruff check --fix .
uvx ruff format .
```

---

## 5. エコシステムの変化

---

### Django 6.0（2025年12月リリース）

**Pythonサポートバージョン**

- 3.12, 3.13, 3.14 のみ
- 3.10, 3.11 は Django 5.2 が最後

**主な変更点**

- QuerySetの新しいフェッチモード
- 複合主キーの改善
- レガシーAPIの削除

**Django 20周年**

---

### その他のエコシステム動向

**uWSGI の終焉**

- 開発終了・メンテナンス停止
- 代替：uvicorn, Hypercorn, Granian（Rust製）

**pandas 3.0 の議論**

- PyArrow-backed dtypesをデフォルト化検討中
- メモリ削減・パフォーマンス向上
- DuckDB, Polars との相互運用性向上

**NumPy**

- Free-threaded Python対応が進行中

---

### AIコーディングツールの浸透

**JetBrains調査（2025年）**

- 開発者の **49%** がAIコーディングエージェントを試す予定
- 2024年時点で **44%** が日常的に使用

> 「AIを使いこなせない開発者は採用できない」
> — 大手テック企業のプログラムマネージャー

**学習リソースの変化**

1. ドキュメント（1位）
2. YouTube（51%）
3. オンラインコース

---

## 6. 今後の展望

---

### Python 3.15 開発中

**2026年10月リリース予定**

**現時点で確認されている機能**

- **PEP 686**：UTF-8をデフォルトエンコーディングに
- **PEP 799**：新しいプロファイリングAPI
- **PEP 810**：Lazy Imports（検討中）

**アルファスケジュール**

- 3.15.0a1：2025年10月14日
- 3.15.0a2：2025年11月19日
- 3.15.0a3：2025年12月16日

---

### Free-threaded Python の今後

**3段階の安定化計画**

| フェーズ | 状態 | 説明 |
|----------|------|------|
| Phase 1 | 完了 | 実験的サポート（3.13） |
| Phase 2 | **現在** | 公式サポート・任意有効化（3.14） |
| Phase 3 | 将来 | デフォルト有効化 |

**移行に向けた課題**

- 拡張モジュールの対応（Cython, pybind11, PyO3）
- サードパーティライブラリの検証
- シングルスレッド性能の改善継続

---

### アクションアイテム

**今すぐやるべきこと**

1. Python 3.9 以前を使っている場合は **3.13/3.14へ移行**
2. **uv** を試してみる（`curl -LsSf https://astral.sh/uv/install.sh | sh`）
3. **Ruff** でコード品質を向上（`uvx ruff check .`）

**検討すべきこと**

4. Free-threaded Python の検証（CPU集約型処理がある場合）
5. t-strings の活用検討（セキュリティ向上）
6. Django 6.0 移行計画（Django利用者）

---

## まとめ

---

### 2025年 Python 動向まとめ

| カテゴリ | ハイライト |
|----------|-----------|
| 人気度 | TIOBE史上最高 25.35% |
| リリース | Python 3.14（10月）、Django 6.0（12月） |
| EOL | Python 3.9（10月31日終了） |
| 新機能 | t-strings, No-GIL公式化, concurrent.interpreters |
| ツール | uv/Ruff等 Rust製ツールが標準化 |
| 次期 | Python 3.15 アルファ進行中 |

---

### 参考リンク一覧

**公式ドキュメント**

- [What's New in Python 3.14](https://docs.python.org/3/whatsnew/3.14.html)
- [Python Release Schedule](https://devguide.python.org/versions/)
- [PEP 750 - Template Strings](https://peps.python.org/pep-0750/)
- [PEP 779 - Free-threaded Python](https://peps.python.org/pep-0779/)
- [PEP 745 - Python 3.14 Release Schedule](https://peps.python.org/pep-0745/)

**ツール**

- [uv Documentation](https://docs.astral.sh/uv/)
- [Ruff Documentation](https://docs.astral.sh/ruff/)
- [Astral Blog](https://astral.sh/blog)

**ニュース・調査**

- [Real Python News](https://realpython.com/python-news/)
- [JetBrains - The State of Python 2025](https://blog.jetbrains.com/pycharm/2025/08/the-state-of-python-2025/)
- [TIOBE Index](https://www.tiobe.com/tiobe-index/)
- [InfoWorld Python News](https://www.infoworld.com/category/python/)

---

# ありがとうございました
