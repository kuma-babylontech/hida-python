---
title: "Python 3.15リリース！新機能と3.10からの歩み"
date: 2026-10-18
description: "2026年10月にリリースされたPython 3.15の新機能（lazy import・frozendict・sentinel・UTF-8デフォルト・Tachyonプロファイラ・JIT）を、これまでの書き方と比べながら初学者向けに紹介します。3.10〜3.15を実際に動かした比較つき。"
tags:
  - Python
  - Python 3.15
  - 新機能
  - パフォーマンス
author: "kuma"
---

# Python 3.15リリース！

新機能と3.10からの歩み

飛騨高山Pythonの会

---

## 今日の話

1. Python 3.15ってどんなリリース？
2. 3.10→3.15で何が変わった？（実測）
3. 3.15の目玉機能（これまでとの比較つき）
4. 開発体験の改善
5. アップグレードの注意点
6. AIと一緒に3.15を使うとき

> デモコードは `demo/2026-10-python315/` にあります。
> 数字はすべて手元のMacBook（Apple Silicon）で実行した結果です

---

## 1. Python 3.15ってどんなリリース？

---

### リリース概要

| 項目 | 内容 |
|---|---|
| リリース日 | **2026年10月9日**（予定より1週間延期。rc3を追加） |
| リリースマネージャー | Hugo van Kemenade（リリース作業のまとめ役） |
| バグ修正サポート | 約2年（2028年10月ごろまで） |
| セキュリティサポート | 5年（2031年10月まで） |

毎年10月に新バージョンが出るリズムは、3.9から変わらず

--

### 3.15を一言でいうと

毎日書くコードが**少しずつ楽になる**リリース

| 新機能 | ひとことで |
|---|---|
| lazy import | 使うときまでモジュールを読み込まない。起動が速くなる |
| frozendict | 書き換えられない辞書（dict） |
| sentinel | 「値が渡されなかった」を表す専用の目印 |
| 内包表記の `*` | リストのリストを1行で平らにできる |
| UTF-8がデフォルト | WindowsとMacで、ファイルの読み書きの結果がそろう |
| Tachyon | 動いているプログラムの遅い場所を外から調べる道具 |
| JIT | よく動く部分をその場で機械語にして速くする仕組み |

--

### サポート中のバージョン（2026年10月時点）

| バージョン | リリース | サポート終了 | 状態 |
|---|---|---|---|
| **3.15** | 2026年10月 | 2031年10月 | **最新** |
| 3.14 | 2025年10月 | 2030年10月 | バグ修正 |
| 3.13 | 2024年10月 | 2029年10月 | セキュリティのみ |
| 3.12 | 2023年10月 | 2028年10月 | セキュリティのみ |
| 3.11 | 2022年10月 | 2027年10月 | セキュリティのみ |
| ~~3.10~~ | 2021年10月 | **2026年10月** | **サポート終了** |

サポートが終わると、セキュリティの穴が見つかっても修正版が出ない。3.10を使っている人は今がアップグレードのタイミング

---

## 2. 3.10→3.15で何が変わった？

---

### 毎年増えてきた機能（実際に動かして確認）

| 機能 | 追加 | 3.10 | 3.11 | 3.12 | 3.13 | 3.14 | 3.15 |
|---|---|---|---|---|---|---|---|
| `except*` / ExceptionGroup | 3.11 | × | ○ | ○ | ○ | ○ | ○ |
| `type` 文・ジェネリクス構文 | 3.12 | × | × | ○ | ○ | ○ | ○ |
| `copy.replace()` | 3.13 | × | × | × | ○ | ○ | ○ |
| t-string | 3.14 | × | × | × | × | ○ | ○ |
| **lazy import** | 3.15 | × | × | × | × | × | ○ |
| **frozendict / sentinel** | 3.15 | × | × | × | × | × | ○ |
| 内包表記の `*` アンパック | 3.15 | × | × | × | × | × | ○ |

○は動いた、×は動かなかった。各バージョンでコード片を実行して判定（`06_compare_versions.py`）

--

### 各バージョンのテーマ

| バージョン | ひとことで |
|---|---|
| 3.11 | **速くなった**（Faster CPython）・エラーの場所を詳しく表示 |
| 3.12 | **型ヒントの書き方**が簡単に（`type` 文・`def f[T]()`） |
| 3.13 | 対話モード（REPL）が新しく・**GILなし版**とJITが試験的に登場 |
| 3.14 | **t-string**（安全に文字列を組み立てる）・GILなし版が正式サポート |
| 3.15 | **lazy import**・frozendict・UTF-8・**JITが実用レベル**へ |

GIL：Pythonが同時に1つのスレッドしか動かさないための仕組み。外すと複数のCPUコアを同時に使える

--

### 速さはどう変わった？（実測）

同じ純Pythonのコードを5回ずつ実行（秒・中央値。小さいほど速い）

| バージョン | nbody | primes | objects | strings | 合計 | 3.10比 |
|---|---|---|---|---|---|---|
| 3.10 | 0.674 | 1.156 | 0.684 | 0.198 | 2.712 | 1.00x |
| 3.11 | 0.489 | 0.721 | 0.474 | 0.157 | 1.840 | **1.47x** |
| 3.12 | 0.400 | 0.771 | 0.464 | 0.166 | 1.802 | 1.51x |
| 3.13 | 0.406 | 1.125 | 0.340 | 0.167 | 2.039 | 1.33x |
| 3.14 | 0.429 | 0.706 | 0.354 | 0.177 | 1.666 | 1.63x |
| 3.15 | 0.437 | 0.664 | 0.347 | 0.175 | 1.622 | **1.67x** |
| **3.15 + JIT** | 0.305 | 0.376 | 0.327 | 0.157 | 1.166 | **2.33x** |

macOS / Apple Silicon、uv管理のCPythonビルドで計測（`bench_workload.py`）

--

### 速さの読み方

- **3.11で一気に1.5倍**。それ以降はインタプリタ単体だと少しずつ
- 3.13は `primes`（整数のwhileループ）だけ遅かった
  - このビルドで何度測っても再現。原因までは追えていません
- **3.15でJITを有効にすると、さらに1.4倍**
  - JIT：よく実行される部分を、実行中に機械語へ変換して速くする仕組み
  - 数値計算のループ（nbody・primes）で速くなる。文字列処理（strings）はほぼ変わらない

```bash
PYTHON_JIT=1 python3.15 my_script.py   # JIT はまだ既定でオフ
```

公式の数字：x86-64 Linuxで7〜8%、macOS（AArch64）で11〜12%の高速化（幾何平均）

---

## 3. 3.15の目玉機能

これまでの書き方と比べて、何がうれしいのか

---

### lazy import（PEP 810）

import：ほかのモジュール（ファイル）の機能を読み込むこと。読み込みには時間がかかる

```python
lazy import json
lazy from pathlib import Path

print("起動しました")       # この時点では json も pathlib も読み込まれていない

data = json.loads("{}")    # ここで初めて json を読み込む
```

- `lazy` を付けたimportは、**最初に使われるまで読み込まれない**
- 使われなければ一度も読み込まれない

--

### lazy import：これまでとの違い

```python
# これまで：起動を速くしたいときは、import を関数の中に移していた
def export_csv(rows):
    import csv              # この関数が呼ばれるまで読み込まない
    ...

# 3.15：import はファイルの先頭にまとめたまま、読み込みだけ遅らせられる
lazy import csv
```

**うれしいこと**

- 使わない機能のぶん、**起動が速くなる**（次のページで実測）
- importを先頭にまとめたままなので、何を使っているか一目で分かる
- 書き換えは `lazy` を足すだけ

--

### lazy importの効果（実測）

重いモジュールを8個importするCLIで `--help` だけ実行

```text
Python 3.15.0 / --help の起動時間（中央値・20回）
  import なし   :   18.4 ms
  通常の import :   79.2 ms
  lazy import   :   18.4 ms
  → import 部分 60.8 ms が 0.0 ms に
  読み込まれたモジュール数: 通常 221 / lazy 56
```

`--help` やサブコマンドの多いCLIほど**効果が大きい**

（`01_lazy_imports.py`）

--

### lazy importのルール

- 書けるのは**モジュールの一番外側だけ**
  - 関数・クラスの中、`try` / `except` の中は `SyntaxError`
- `lazy from x import *` は不可
- `lazy` は特定の場所でだけキーワードになる「ソフトキーワード」。`lazy` という変数名は今までどおり使える
- 全体をまとめて切り替えることもできる

```bash
python -X lazy_imports=all app.py        # すべての import を lazy に
```

- 古いバージョンでも動かしたいライブラリ向けの書き方もある

```python
__lazy_modules__ = ["json", "pathlib"]   # 3.15 では lazy、それ以前は通常の import
import json
```

--

### frozendict（PEP 814）

**書き換えられない辞書**（dict）が組み込みに

```python
>>> a = frozendict(x=1, y=2)
>>> a["z"] = 3
TypeError: 'frozendict' object does not support item assignment
>>> a == frozendict(y=2, x=1)       # 順番が違っても中身が同じなら等しい
True
>>> {a: "OK"}                       # 辞書のキーにできる
{frozendict({'x': 1, 'y': 2}): 'OK'}
```

- ハッシュ：値から計算する番号。これが計算できる値だけが、辞書のキーや `set` の要素になれる
- 書き換えられないので、frozendictはハッシュを計算できる

--

### frozendict：これまでとの違い

| できること | dict | MappingProxyType<br>（これまでの代わり） | frozendict |
|---|---|---|---|
| 中身を書き換える | できる | 直接はできない | できない |
| 元の辞書の変更が反映される | − | **反映されてしまう** | − |
| 辞書のキーや `set` に入れる | できない | できない | **できる** |
| `@functools.cache` の引数にする | できない | できない | **できる** |

**うれしいこと**

- 設定値などを**うっかり書き換えるバグ**を防げる
- 辞書を、キャッシュのキーや別の辞書のキーとして使える

`MappingProxyType` の列は3.14で実際に動かして確認

--

### frozendictの使いどころ

```python
import functools, json

# json に array_hook が増えたので、中までまるごと書き換え不可にして読める
config = json.loads(text, object_hook=frozendict, array_hook=tuple)
# frozendict({'db': frozendict({'host': 'localhost', 'port': 5432}),
#             'features': ('search', 'export')})

@functools.cache                  # 結果を覚えておき、同じ引数なら計算を省く
def connection_string(db: frozendict) -> str:
    return f"postgresql://{db['host']}:{db['port']}"

connection_string(config["db"])   # dict だとエラー。frozendict なら OK
```

- `dict` の仲間（サブクラス）ではないので、型を調べるときは `Mapping` を使う

（`02_frozendict.py`）

--

### sentinel（PEP 661）：なぜ必要？

番兵（sentinel）：「値が渡されなかった」ことを表す専用の目印

```python
# よくある書き方：省略されたら None
def get(key, default=None):
    ...

get("age")          # 省略された
get("age", None)    # None を渡した
# → 関数の中からは、どちらも default が None に見えて区別できない
```

「省略されたらエラーにしたい。でも `None` を既定値として渡すのは許したい」ときに困る

--

### sentinel：これまでとの違い

```python
MISSING = sentinel("MISSING")       # 3.15

def get(key, default=MISSING):
    if key in store:
        return store[key]
    if default is MISSING:          # 省略されたときだけエラー
        raise KeyError(key)
    return default                  # None を既定値に指定できる
```

| | `object()`（これまでの定番） | `sentinel()` |
|---|---|---|
| 表示（エラー時など） | `<object object at 0x...>` | `MISSING` |
| コピー後も同じもの？ | × 別物になる | ○ |
| 型ヒント | 書きにくい | `int \| MISSING` |

**うれしいこと**：エラー表示が読みやすく、コピーしても目印のまま使える

--

### 内包表記で `*` / `**`（PEP 798）

内包表記：`[x * 2 for x in nums]` のように、リストを1行で作る書き方

```python
rows = [[1, 2], [3], [4, 5]]

# これまで：for が2つ。どちらを先に書くか毎回迷う
[x for row in rows for x in row]

# 3.15：「row の中身を広げて並べる」と、そのまま読める
[*row for row in rows]              # [1, 2, 3, 4, 5]
{*s for s in sets}                  # 集合をまとめる
{**d for d in dicts}                # 辞書をまとめる（同じキーは後が勝つ）
```

**うれしいこと**：`f(*args)` と同じ `*` で、リスト・集合・辞書をそろえて書ける

--

### UTF-8がデフォルトに（PEP 686）

エンコーディング：文字をバイト列に変える決まり。書いたときと違う決まりで読むと文字化けする

| `open("memo.txt")` の読み方 | これまで | 3.15 |
|---|---|---|
| 日本語Windows | cp932（Shift_JIS系） | **UTF-8** |
| macOS / Linux | ほぼUTF-8 | UTF-8 |

**うれしいこと**

- Macで書いたコードが、Windowsで `UnicodeDecodeError` になることがなくなる
- `encoding=` を書き忘れても、どのOSでも同じ結果になる

--

### UTF-8デフォルトの注意点

- **日本語Windowsユーザーには大きな変更**
- 逆に、**cp932のファイルをエンコーディング未指定で読んでいたコードは、正しく読めなくなる**
  - Excelが書き出したCSVなどで起きやすい
- 対策：`encoding=` を明示する

```python
open("data.csv", encoding="cp932")      # Shift_JIS 系のファイル
open("memo.txt", encoding="utf-8")      # 3.14 以前でも同じ結果にしたいとき
```

- 一時的に元に戻すなら `PYTHONUTF8=0` / `-X utf8=0`

---

## 4. 開発体験の改善

---

### Tachyon：新しいプロファイラ（PEP 799）

プロファイラ：プログラムのどこに時間がかかっているかを調べる道具

| | cProfile（これまで） | Tachyon（3.15） |
|---|---|---|
| 調べ方 | 関数の呼び出しをすべて記録 | 一定間隔で「今どこを実行中か」を覗く（サンプリング） |
| 調べられるプログラムへの負荷 | 大きい（今回のデモで0.63秒→1.42秒） | 小さい（外から覗くだけ） |
| 動いているプロセスに後から接続 | できない | **できる** |

**うれしいこと**：本番で遅くなったプログラムを止めずに調べられる

--

### Tachyonの使い方

```bash
# 実行してフレームグラフ（どこで時間を使ったかの図）を作る
python -m profiling.sampling run --flamegraph -o flame.html script.py

# 動いているプロセスに接続（top のような画面）
python -m profiling.sampling attach --live 1234
```

- 最大100万回/秒でサンプリングできる
- `cProfile` はなくならない。`profiling.tracing` という名前でも使える

--

### Tachyonのフレームグラフ

![Tachyon のフレームグラフ](assets/tachyon-flamegraph.png)

横幅が長いほど時間を使っている。`slow_word_count` が全体の約7割で、行番号まで分かる

--

### Tachyonの落とし穴：macOSではsudoが要る

```text
🔒 Permission Error: Unable to access process memory on macOS
Tachyon needs elevated permissions to profile processes.
```

- 他プロセスのメモリを読む仕組みなので、**macOSでは `sudo`（管理者権限）が必要**
- 今回はLinuxのDockerコンテナ（rootで実行）で計測した

```bash
# 今回は Docker で計測
docker run --rm -v "$PWD":/work -w /work python:3.15-slim \
  python -m profiling.sampling run --flamegraph -o output/flame.html 05_profile_target.py
```

--

### エラーメッセージ：これまでとの違い

他の言語のメソッド名を使うと、Pythonでの書き方をヒントとして出す

| 書いたコード | 3.14まで | 3.15で増えたヒント |
|---|---|---|
| `[].push(1)` | `'list' object has no attribute 'push'` | `Did you mean '.append'?` |
| `"a".toUpperCase()` | `'str' object has no attribute 'toUpperCase'` | `Did you mean '.upper'?` |
| `{}.put("k", 1)` | `'dict' object has no attribute 'put'` | `Use d[k] = v.` |
| `(1, 2).append(3)` | `'tuple' object has no attribute 'append'` | `Did you mean to use a 'list' object?` |

**うれしいこと**：JavaScriptやJavaから来た人も、調べずに直し方が分かる

--

### その他の便利な変更

| 変更 | 内容 |
|---|---|
| `re.prefixmatch()` | `re.match()`（先頭から一致を調べる）の、名前で意味が分かる別名 |
| `TypedDict(closed=True)` | 決めたキー以外を入れると、型チェッカーが指摘する |
| `math.integer` | `gcd`（最大公約数）など、整数用の関数をまとめた新モジュール |
| `asyncio.TaskGroup.cancel()` | 同時に動かしている処理をまとめて止める |
| `tomllib` | 設定ファイル形式TOMLの新しい版（1.1）に対応 |
| `base64` | エンコードが2倍・デコードが3倍速く |
| REPL・CLI | 補完やヘルプに色がつく |

--

### GILなし版（free-threading）の続報

GILを外したPython。複数のスレッドが本当に同時に動くので、CPUのコアを使い切れる

| | 3.13 | 3.14 | 3.15 |
|---|---|---|---|
| 位置づけ | 試験的 | 正式サポート（任意） | 正式サポート（任意） |
| C拡張の配布 | バージョンごとにビルド | バージョンごとにビルド | **安定ABI（`abi3t`）** で1回のビルドで済む |
| macOS公式インストーラ | 選択 | 選択 | **既定でインストール** |

C拡張：numpyなどC言語で書かれた部品。ライブラリの作者が対応しやすくなり、GILなし版で使えるライブラリが増えていきそう

---

## 5. アップグレードの注意点

---

### 削除されたもの（主なもの）

| モジュール | 削除 | 代わり |
|---|---|---|
| `http.server` | `CGIHTTPRequestHandler`・`--cgi` | なし |
| `sre_compile` など | `sre_*` モジュール | `re` |
| `importlib` | `load_module()` | `exec_module()` |
| `pathlib` | `PurePath.is_reserved()` | `os.path.isreserved()` |
| `typing` | `NamedTuple("P", x=int)` 形式 | クラス構文 |
| `datetime` | 年なしの `strptime("%d")` | 年を含める（`ValueError` に） |

どれも以前のバージョンから「将来消える」と警告されていたもの。古いライブラリを使っているときに影響しやすい

--

### アップグレード前のチェックリスト

- [ ] `open()` / `read_text()` に **`encoding=` を書いているか**（特にWindows・cp932）
- [ ] `isinstance(x, dict)` で受けている所にfrozendictが来ないか（来るなら `Mapping` で判定する）
- [ ] 前のページの削除APIを使っていないか
- [ ] 依存ライブラリが3.15用のパッケージ（ホイール）を出しているか
- [ ] `profile` モジュールを使っていないか（3.17で削除予定）
- [ ] `asyncio` のイベントループポリシーを使っていないか（3.16で削除予定）

```bash
python3.15 -W error::DeprecationWarning -m pytest   # 非推奨の警告をエラーにして洗い出す
```

--

### 試してみるならuvが早い

uv：Python本体とライブラリをまとめて管理できるツール

```bash
uv python install 3.15
uv run --python 3.15 python -c "print(frozendict(a=1))"

# 既存プロジェクトを 3.15 で試す
uv venv --python 3.15 .venv-315
uv pip install -r requirements.txt --python .venv-315
```

- uv自体が古いと3.15の正式版が見つからず、**alpha版（開発途中の版）が入る**
  - 今回は半年前のuvで `3.15.0a7` が入った。`uv self update` で更新しておく

---

## 6. AIと一緒に3.15を使うとき

---

### AIは3.15を知らない前提で使う

- 学習データが3.15のリリースより前のモデルが多い
  - 新しい書き方（lazy import・frozendict・内包表記の `*`）を**誤りとして直す**ことがある
  - 古い書き方（`object()` の番兵、二重forの内包表記）を提案しがち
- 前提はCLAUDE.mdなどに短く書いておく

```markdown
- Python 3.15前提。frozendict・sentinel・lazy importを使ってよい
- open() には encoding= を必ず書く
```

- エージェントに環境を作らせたら `python -VV` で**正式版か確かめる**
- lintも新しくしておく。最新のruff 0.17.1とmypy 2.4.0は新構文を扱えた
  - 古いツールがエラーを出すと、エージェントが正しいコードを書き換えるおそれがある

--

### AIが書きがちなコードとの組み合わせ

| AIに任せがちなこと | 3.15での注意 |
|---|---|
| importを全部lazyにする | import時の登録処理が動かない。`ImportError` も使うときまで出ない |
| `isinstance(x, dict)` で判定 | frozendictは弾かれる。`Mapping` で判定させる |
| `encoding=` の省略 | 3.15ではUTF-8だが、3.14以前の日本語Windowsではcp932で読まれる |
| 性能の調査 | Tachyonで外から計測させられる。ただしmacOSではsudoが要る |
| 「速くなります」という説明 | 処理の中身しだい。各バージョンで**実測させる** |

lazyにするのは、起動時間など効果を測れた箇所に絞る

---

## まとめ

---

### これまでと3.15の比較

| 機能 | これまで | 3.15 |
|---|---|---|
| 起動を速くする | importを関数の中に移す | 先頭で `lazy import` |
| 書き換えられない辞書 | `MappingProxyType`（キーにできない） | `frozendict` |
| 「省略された」の目印 | `object()`（表示が読みにくい） | `sentinel("MISSING")` |
| リストを平らにする | `[x for row in rows for x in row]` | `[*row for row in rows]` |
| ファイルの文字コード | OSごとに違う | どこでもUTF-8 |
| 遅い場所を探す | cProfile（遅くなる・後から接続できない） | Tachyon |

--

### Python 3.15まとめ

| テーマ | ポイント |
|---|---|
| 書きやすさ | lazy import・frozendict・sentinel・内包表記の `*` |
| 移植性 | **UTF-8がデフォルト**（特にWindowsで影響が大きい） |
| 速さ | 3.10比1.67倍、**JITを入れると2.33倍**（今回の実測） |
| 調べやすさ | Tachyonプロファイラ・親切なエラーメッセージ |
| 気をつけること | `encoding` の明示・削除API・3.10はサポート終了 |
| AIと使うとき | 3.15前提を伝える・バージョンを確かめる・実測させる |

--

### 参考リンク

- [What's New In Python 3.15](https://docs.python.org/3.15/whatsnew/3.15.html)
- [PEP 790 – Python 3.15 Release Schedule](https://peps.python.org/pep-0790/)
- [PEP 810 – Explicit lazy imports](https://peps.python.org/pep-0810/)
- [PEP 814 – Add frozendict built-in type](https://peps.python.org/pep-0814/)
- [PEP 661 – Sentinel Values](https://peps.python.org/pep-0661/)
- [PEP 798 – Unpacking in Comprehensions](https://peps.python.org/pep-0798/)
- [PEP 686 – Make UTF-8 mode default](https://peps.python.org/pep-0686/)
- [PEP 799 – A dedicated profiling package](https://peps.python.org/pep-0799/)

---

# ありがとうございました

デモ：`demo/2026-10-python315/`
