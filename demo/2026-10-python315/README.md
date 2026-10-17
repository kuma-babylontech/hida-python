# Python 3.15新機能デモ

スライド「Python 3.15リリース！新機能と3.10からの歩み」のデモ。標準ライブラリだけで動く（テストにpytestのみ使う）。

## 準備

```bash
uv python install 3.10 3.11 3.12 3.13 3.14 3.15   # 06 の比較に使う
uv venv -p 3.15 .venv && uv pip install -p .venv -r requirements.txt
```

uvが古いと3.15の正式版が見つからず、alpha版が入る。`uv self update` してから実行する。

## スクリプト

| ファイル | 内容 |
|---|---|
| `01_lazy_imports.py` | lazy import（PEP 810）でCLIの起動時間とモジュール数を比較 |
| `02_frozendict.py` | frozendict（PEP 814）。JSONを中まで不変で読む・`@cache` の引数に使う |
| `03_sentinel.py` | sentinel（PEP 661）で「未指定」と `None` を区別 |
| `04_small_changes.py` | 内包表記の `*`・UTF-8デフォルト・エラーメッセージ・`re.prefixmatch` など |
| `05_profile_target.py` | Tachyon（PEP 799）でプロファイルするための重い処理 |
| `06_compare_versions.py` | 3.10〜3.15で機能の有無と速度を比較（3.15はJITあり/なし）。結果は `output/compare.md` |

```bash
.venv/bin/python 01_lazy_imports.py
.venv/bin/python 06_compare_versions.py        # 数分かかる。--features で機能表だけ
.venv/bin/python -m pytest
```

## TachyonはmacOSだとsudoが要る

他プロセスのメモリを読むため、macOSでは `Permission Error: Unable to access process memory` になる。
`sudo -E` を付けるか、Dockerで実行する（スライドの図はDockerで作成した）。

```bash
docker run --rm -v "$PWD":/work -w /work python:3.15-slim \
  python -m profiling.sampling run --flamegraph -o output/flame.html 05_profile_target.py
```
