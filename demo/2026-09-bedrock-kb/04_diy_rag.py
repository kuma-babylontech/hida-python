"""④ 同じことを自分で書く — Knowledge Bases を使わない RAG。

Knowledge Bases が隠している4つの工程を、Python で素朴に書き下す。

  1. 取り込み  … slides/*/slide.md を読む
  2. 分割      … スライド区切り（---）でチャンクにする
  3. 埋め込み  … Titan Embeddings でベクトルにする
  4. 検索      … numpy でコサイン類似度を計算して上位を取る
  （5. 生成    … 引いた文章をプロンプトに詰めて Claude に渡す）

これで全部。ライブラリは boto3 と numpy だけ。
"""

import json

import numpy as np

import common

TOP_K = 3


# --- 1. 取り込み ------------------------------------------------------------
def load_documents():
    """slides/*/slide.md を読み込む（この回の発表資料そのものは除く）。"""
    documents = []
    for path in sorted(common.SLIDES_DIR.glob("*/slide.md")):
        if path.parent.name in common.EXCLUDED_SLIDES:
            continue
        documents.append({"name": path.parent.name, "text": path.read_text(encoding="utf-8")})
    return documents


# --- 2. 分割 ----------------------------------------------------------------
def split_into_chunks(documents, min_chars=80):
    """スライドの区切り（---）でチャンクに割る。

    区切りが自然に存在する資料なら、これだけで十分に機能する。
    Knowledge Bases では「何文字で割るか」を設定値で選ぶ部分にあたる。
    """
    chunks = []
    for document in documents:
        for part in document["text"].split("\n---\n"):
            text = part.strip()
            if len(text) >= min_chars:
                chunks.append({"source": document["name"], "text": text})
    return chunks


# --- 3. 埋め込み ------------------------------------------------------------
def embed(client, text):
    """Titan Embeddings で文章を 1024 次元のベクトルにする。"""
    response = client.invoke_model(
        modelId=common.EMBED_MODEL_ID,
        body=json.dumps({"inputText": text}),
    )
    return json.loads(response["body"].read())["embedding"]


def embed_all(chunks):
    client = common.bedrock_runtime()
    return np.array([embed(client, chunk["text"]) for chunk in chunks], dtype=np.float32)


# --- 4. 検索 ----------------------------------------------------------------
def search(question_vector, chunk_vectors, chunks, top_k=TOP_K):
    """コサイン類似度で近いチャンクを取る。これがベクトル検索の中身。"""
    normalized = chunk_vectors / np.linalg.norm(chunk_vectors, axis=1, keepdims=True)
    query = question_vector / np.linalg.norm(question_vector)
    scores = normalized @ query
    ranking = np.argsort(scores)[::-1][:top_k]
    return [(chunks[i], float(scores[i])) for i in ranking]


# --- 5. 生成 ----------------------------------------------------------------
PROMPT = """あなたは飛騨高山Pythonの会の発表資料に答えるアシスタントです。
以下の<資料>はすべて、この会の過去の発表スライドです。
<資料>だけを根拠に質問へ答えてください。資料に無いことは「資料にありません」と答えてください。

<資料>
{context}
</資料>

質問: {question}"""


def generate(hits, question):
    context = "\n\n".join(f"[{h['source']}]\n{h['text']}" for h, _ in hits)
    prompt = PROMPT.format(context=context, question=question)
    return common.ask_claude(common.bedrock_runtime(), prompt)


def main():
    common.banner("④ 自前RAG — Knowledge Bases を使わずに書く")
    print(f"質問: {common.QUESTION}")

    chunks = split_into_chunks(load_documents())
    print(f"\n1-2. 取り込み＋分割: {len(chunks)} チャンク")

    cache = common.load_snapshot("04_diy_rag")
    try:
        chunk_vectors = embed_all(chunks)
        print(f"3. 埋め込み: {chunk_vectors.shape[0]} 件 × {chunk_vectors.shape[1]} 次元")
        question_vector = np.array(embed(common.bedrock_runtime(), common.QUESTION), dtype=np.float32)
        hits = search(question_vector, chunk_vectors, chunks)
        answer = generate(hits, common.QUESTION)
        common.save_snapshot(
            "04_diy_rag",
            {
                "question": common.QUESTION,
                "chunk_count": len(chunks),
                "hits": [{"source": h["source"], "score": round(s, 4)} for h, s in hits],
                "answer": answer,
            },
        )
    except Exception as exc:
        if cache is None:
            raise
        print(f"[AWS を呼べないためスナップショットを使用: {type(exc).__name__}]")
        hits = [({"source": h["source"], "text": ""}, h["score"]) for h in cache["hits"]]
        answer = cache["answer"]

    print("\n4. 検索の結果:")
    for chunk, score in hits:
        print(f"   score={score:.4f}  {chunk['source']}")

    print("\n5. 生成:")
    print(answer)
    print("\n→ 書いたのは約100行。分割の仕方もスコアも、全部手元にある。")


if __name__ == "__main__":
    main()
