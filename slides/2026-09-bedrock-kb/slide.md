---
title: "Amazon Bedrock Knowledge Bases で作るRAG"
date: 2026-09-20
description: "この会の過去の発表スライドを資料にして、自然文で質問できるようにする。Bedrock Knowledge Bases に任せる作り方と、同じものを boto3 と numpy だけで自分で書く作り方を比べます。"
tags:
  - AWS
  - Bedrock
  - RAG
  - LLM
  - boto3
author: "kuma"
---

# Amazon Bedrock<br>Knowledge Bases で作るRAG

## どこまで任せて、どこから自分で書くか

飛騨高山Pythonの会 #80 / 2026年9月

---

## 今日のアジェンダ

1. RAG ってなに？
2. RAG を5つの工程に分解する
3. Knowledge Bases に任せてみる
4. 同じものを自分で書いてみる
5. 任せる / 書く の分かれ目
6. ハマったところ

**題材**: この会の過去の発表スライド4本

---

## はじめに

--

### 今回は不動産シリーズをお休みします

- 予告していた **Part 3（機械学習で価格予測）** は次回に
- 別の案件で Bedrock を触っていて、面白かったので先にこちらを

--

### 今日の題材

**この勉強会の過去の発表スライド**に質問できるようにする

| 回 | テーマ |
|---|---|
| 2025年12月 | 2025年 Python動向振り返り |
| 2026年2月 | OpenAPI × FastAPI 入門 |
| 2026年4月 | 不動産データ分析 Part 1 |
| 2026年6月 | 不動産データ分析 Part 2 |

GitHub にある Markdown 4本、あわせて **約60KB**

---

## RAG ってなに？

--

### まず、そのまま聞いてみる

```python
import boto3

client = boto3.client("bedrock-runtime", region_name="ap-northeast-1")

response = client.converse(
    modelId="jp.anthropic.claude-haiku-4-5-20251001-v1:0",
    messages=[{"role": "user", "content": [{"text": 質問}]}],
)
print(response["output"]["message"]["content"][0]["text"])
```

**質問**: 「飛騨高山Pythonの会の不動産データ分析で、
　　　　　重回帰分析の決定係数R²はいくつでしたか？」

--

### 答えられない

> 申し訳ございませんが、「飛騨高山Pythonの会」の不動産データ分析における
> 決定係数R²の具体的な値についての情報を持っていません。

当然で、**学習データに入っていない**

- LLM が知っているのは「学習した時点の、公開されている知識」だけ
- 社内資料・手元の資料は入っていない

--

### 知らないことを答えさせる2つの方法

| 方法 | やること | 手間 |
|---|---|---|
| ファインチューニング | モデル自体を追加学習させる | 重い・資料が変わるたび再学習 |
| **RAG** | **質問のたびに資料を探して渡す** | **軽い・資料を差し替えるだけ** |

**RAG** = Retrieval-Augmented Generation
（検索で補強した生成）

--

### RAG の正体

やっていることは、拍子抜けするほど単純

```text
1. 質問に関係ありそうな文章を、資料の中から探す
2. 見つけた文章をプロンプトに貼る
3. 「これを読んで答えて」と LLM に渡す
```

→ **「カンニングペーパーを作って渡す」** だけ

難しいのは「関係ありそうな文章を探す」ところ

---

## RAG を5つの工程に分解する

--

### 5つの工程

| # | 工程 | やること |
|---|---|---|
| 1 | 取り込み | ファイルを読む |
| 2 | 分割 | 長い資料をチャンクに切る |
| 3 | 埋め込み | 文章をベクトル（数字の並び）にする |
| 4 | 検索 | 質問に近いチャンクを取り出す |
| 5 | 生成 | 見つけた文章を添えて LLM に聞く |

今日はこの5つを **地図** として使います

--

### 「埋め込み」ってなに？

文章を **数字の並び（ベクトル）** に変換すること

```python
response = client.invoke_model(
    modelId="amazon.titan-embed-text-v2:0",
    body=json.dumps({"inputText": "重回帰分析の決定係数"}),
)
vector = json.loads(response["body"].read())["embedding"]
len(vector)   # → 1024
```

- どんな文章でも **1024個の数字** になる
- **意味が近い文章ほど、ベクトルの向きが近い**

--

### なぜベクトルにするのか

キーワード検索だと取りこぼす

| 質問 | 資料の書き方 | キーワード一致 |
|---|---|---|
| 「決定係数はいくつ？」 | 「R² = 0.488」 | ✗ 一致しない |

ベクトルなら「決定係数」と「R²」が**近い向き**になる

→ 言い回しが違っても引ける

---

## Knowledge Bases に任せてみる

--

### Amazon Bedrock Knowledge Bases

**5工程のうち 1〜4 を AWS がやってくれる** マネージドサービス

```text
S3 に資料を置く
   ↓  「同期」ボタン（または API）
取り込み → 分割 → 埋め込み → ベクトルストアに保存
   ↓
質問を投げると、近いチャンクが返ってくる
```

RAG のコードは **0行**

--

### 用意するもの

| 役割 | 今回使ったもの |
|---|---|
| 資料置き場 | S3 バケット |
| 埋め込みモデル | Titan Text Embeddings V2（1024次元） |
| ベクトルストア | **S3 Vectors** |
| 回答を書くモデル | Claude Haiku 4.5 |

作業はコンソールなら数分。
今回はスクリプト化してあります（`setup/provision.sh`）

--

### Python から叩く — クライアントは2つ

```python
import boto3

# 管理する側（KB を作る・同期する）
agent = boto3.client("bedrock-agent")

# 使う側（検索する・答えさせる）
runtime = boto3.client("bedrock-agent-runtime")
```

発表で使うのは下の **`bedrock-agent-runtime`** だけ

--

### ① Retrieve — 検索だけする

```python
response = runtime.retrieve(
    knowledgeBaseId=KB_ID,
    retrievalQuery={"text": 質問},
    retrievalConfiguration={
        "vectorSearchConfiguration": {"numberOfResults": 3}
    },
)
```

生成はしない。**近いチャンクを3件返すだけ**

--

### Retrieve が返すもの

```python
for r in response["retrievalResults"]:
    r["score"]                            # 近さのスコア
    r["location"]["s3Location"]["uri"]    # どのファイルから来たか
    r["content"]["text"]                  # チャンクの本文
```

この3つが揃うと **出典カードが作れる**

- どの資料の
- どのあたりに
- こう書いてあった

--

### ② RetrieveAndGenerate — 検索＋生成

```python
response = runtime.retrieve_and_generate(
    input={"text": 質問},
    retrieveAndGenerateConfiguration={
        "type": "KNOWLEDGE_BASE",
        "knowledgeBaseConfiguration": {
            "knowledgeBaseId": KB_ID,
            "modelArn": MODEL_ARN,
        },
    },
)
response["output"]["text"]   # 回答
response["citations"]        # 根拠にしたチャンク
```

**これ1回で RAG が完成する**

--

### コード解説: 出典は LLM に書かせない

```python
def build_citations(response):
    sources = []
    for citation in response.get("citations", []):
        for ref in citation.get("retrievedReferences", []):
            sources.append(ref["location"]["s3Location"]["uri"])
    return sources
```

- 出典は **`citations` から機械的に組み立てる**
- 回答文の中に LLM が書いた「出典」は使わない

→ LLM に書かせると、**存在しない出典を創作する余地**が残る

---

## 同じものを自分で書いてみる

--

### 使うのは boto3 と numpy だけ

```bash
pip install boto3 numpy
```

Knowledge Bases が隠していた 1〜4 を、そのまま書き下す

--

### 1-2. 取り込みと分割

```python
def load_documents():
    for path in sorted(SLIDES_DIR.glob("*/slide.md")):
        yield {"name": path.parent.name,
               "text": path.read_text(encoding="utf-8")}

def split_into_chunks(documents, min_chars=80):
    chunks = []
    for document in documents:
        for part in document["text"].split("\n---\n"):
            if len(part.strip()) >= min_chars:
                chunks.append({"source": document["name"],
                               "text": part.strip()})
    return chunks
```

スライドは `---` で区切られているので、**そこで割るだけ**

→ 4ファイルが **65チャンク** になった

--

### 3. 埋め込み

```python
def embed(client, text):
    response = client.invoke_model(
        modelId="amazon.titan-embed-text-v2:0",
        body=json.dumps({"inputText": text}),
    )
    return json.loads(response["body"].read())["embedding"]

vectors = np.array([embed(client, c["text"]) for c in chunks])
vectors.shape   # → (65, 1024)
```

65チャンク × 1024次元の行列ができる

--

### 4. 検索 — コサイン類似度

```python
def search(question_vector, chunk_vectors, chunks, top_k=3):
    normalized = chunk_vectors / np.linalg.norm(
        chunk_vectors, axis=1, keepdims=True)
    query = question_vector / np.linalg.norm(question_vector)
    scores = normalized @ query          # 内積 = コサイン類似度
    ranking = np.argsort(scores)[::-1][:top_k]
    return [(chunks[i], float(scores[i])) for i in ranking]
```

--

### コード解説: ベクトル検索の中身

```python
scores = normalized @ query
```

- 長さを1に揃えてから **内積** を取ると、コサイン類似度になる
- 値が大きいほど「向きが近い」＝「意味が近い」
- `argsort` で上位3件を取る

**ベクトル検索と呼ばれているものの正体は、この1行**

--

### 5. 生成 — プロンプトに貼って渡す

```python
PROMPT = """あなたは飛騨高山Pythonの会の発表資料に答えるアシスタントです。
以下の<資料>はすべて、この会の過去の発表スライドです。
<資料>だけを根拠に質問へ答えてください。
資料に無いことは「資料にありません」と答えてください。

<資料>
{context}
</資料>

質問: {question}"""
```

`{context}` に、検索で見つけた3チャンクを貼る

--

### 動かしてみる

```text
1-2. 取り込み＋分割: 65 チャンク
3.   埋め込み: 65 件 × 1024 次元

4. 検索の結果:
   score=0.5126  2026-06-real-estate-regression
   score=0.4793  2026-06-real-estate-regression
   score=0.4113  2026-06-real-estate-regression
```

3件とも **Part 2（回帰分析）** から引けている

--

### 答えが返ってきた

> 重回帰分析の決定係数 **R² = 0.488** です。
>
> これは約 49% のデータのばらつきを説明できることを意味し、
> 単回帰の R² = 0.300（約 30%）から大幅に向上しています。

- 6月の発表資料の数字と一致
- 全部で **約100行**、実行時間は **15秒ほど**

---

## 任せる / 書く の分かれ目

--

### 5工程をどちらが持つか

| # | 工程 | Knowledge Bases | 自前 |
|---|---|---|---|
| 1 | 取り込み | おまかせ | 書く |
| 2 | 分割 | **設定値を選ぶ** | 書く |
| 3 | 埋め込み | **設定値を選ぶ** | 書く |
| 4 | 検索 | **件数を選ぶ** | 書く |
| 5 | 生成 | 書く | 書く |

任せると、**触れるのは設定値だけ**になる

--

### 任せていい場面

- とにかく早く動くものが要る
- 資料が PDF・テキスト中心で、素直に読める
- 運用（再同期・スケール）を持ちたくない

**業務システムとしては、これが正解なことが多い**

--

### 自分で書きたくなる場面

- **表形式の資料（Excel）がある**
  → 標準の読み取りに任せると、行と列の関係が崩れる
  → 前処理を入れたくても、任せている限り手を出せない
- **分割の仕方を変えて精度を比べたい**
  → 選べるのは用意された設定値の範囲だけ
- **出典の見せ方を細かく作り込みたい**
  → 返ってくる位置情報に縛られる

--

### つまり

> 早く動かしたいなら **任せる**
> 中身を調整したい・学びたいなら **書く**

同じ答えにたどり着く。違うのは
**途中に手を入れられるかどうか**

---

## ハマったところ

--

### ① モデルIDをそのまま渡すと落ちる

```python
modelId="anthropic.claude-haiku-4-5-20251001-v1:0"
# ValidationException: The provided model identifier is invalid.
```

正解は **推論プロファイル** を指定する

```python
modelId="jp.anthropic.claude-haiku-4-5-20251001-v1:0"
```

```bash
aws bedrock list-inference-profiles   # 使えるものを確認
```

`jp.` は日本、`apac.` はアジア太平洋でのルーティング

--

### ② ベクトルの次元を合わせる

S3 Vectors のインデックスは、**作るときに次元を決める**

```bash
aws s3vectors create-index \
  --dimension 1024 \
  --distance-metric cosine
```

埋め込みモデルの出力と **ぴったり合っていないと** 取り込みが落ちる

| モデル | 次元 |
|---|---|
| Titan Text Embeddings V2 | 1024（既定） |

--

### ③ 片付けを忘れない

- ベクトルストアは **置いておくだけで課金**される
- 埋め込みと生成は従量なので、試す分には小さい
- 固定費が出るのは**ベクトルストアの選び方**

→ デモ用の環境は `teardown.sh` で消す

```bash
./setup/teardown.sh
```

---

## まとめ

--

### 学んだこと

- **RAG** = 質問のたびに資料を探して、プロンプトに貼るだけ
- **埋め込み** = 文章を1024個の数字にする。意味が近いと向きが近い
- **ベクトル検索** の正体は、正規化してからの内積1行
- **Knowledge Bases** は5工程のうち1〜4を引き受ける
- 出典は **検索結果から機械的に作る**（LLMに書かせない）

--

### 使ったツール

| 用途 | ツール |
|---|---|
| AWS 呼び出し | `boto3` |
| ベクトル計算 | `numpy` |
| 埋め込み | Titan Text Embeddings V2 |
| 生成 | Claude Haiku 4.5（Bedrock） |
| ベクトルストア | S3 Vectors |

--

### 次回予告

## 不動産データ分析 Part 3

- **機械学習で価格を予測する**
- ランダムフォレストで非線形な関係もとらえる
- 統計モデル vs 機械学習、どう使い分ける？

---

## デモコード

GitHub で公開しています

`demo/2026-09-bedrock-kb/`

```text
01_ask_without_rag.py             # RAGなしで聞く
02_kb_retrieve.py                 # Retrieve（検索だけ）
03_kb_retrieve_and_generate.py    # 検索＋生成
04_diy_rag.py                     # 自前RAG（約100行）
05_compare.py                     # 並べて比較
setup/provision.sh                # AWS環境を作る
setup/teardown.sh                 # 片付ける
```

AWS アカウントが無くても、
**実行結果のスナップショット**で同じ出力が出ます

---

# ありがとうございました

質問・フィードバック歓迎です！
