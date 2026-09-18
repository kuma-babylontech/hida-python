"""自前RAG の、AWS を呼ばない部分のテスト。

取り込み・分割・検索は純粋な Python なのでテストできる。
埋め込みと生成だけが Bedrock 呼び出しで、そこは対象外。
"""

import numpy as np


def test_load_documents_reads_all_slides(diy_rag_mod):
    documents = diy_rag_mod.load_documents()
    assert len(documents) >= 4
    assert all(doc["text"].startswith("---") for doc in documents)


def test_split_drops_short_fragments(diy_rag_mod):
    documents = [{"name": "dummy", "text": "短い\n---\n" + "あ" * 200}]
    chunks = diy_rag_mod.split_into_chunks(documents)
    assert len(chunks) == 1
    assert chunks[0]["source"] == "dummy"


def test_split_produces_chunks_from_real_slides(diy_rag_mod):
    chunks = diy_rag_mod.split_into_chunks(diy_rag_mod.load_documents())
    assert len(chunks) > 20
    assert all(chunk["text"] for chunk in chunks)


def test_search_ranks_by_cosine_similarity(diy_rag_mod):
    chunks = [{"source": "a", "text": "a"}, {"source": "b", "text": "b"}, {"source": "c", "text": "c"}]
    vectors = np.array([[1.0, 0.0], [0.0, 1.0], [0.9, 0.1]], dtype=np.float32)
    question = np.array([1.0, 0.0], dtype=np.float32)

    hits = diy_rag_mod.search(question, vectors, chunks, top_k=2)

    assert [chunk["source"] for chunk, _ in hits] == ["a", "c"]
    assert hits[0][1] > hits[1][1]


def test_prompt_includes_context_and_question(diy_rag_mod):
    hits = [({"source": "slide-1", "text": "R² = 0.488"}, 0.9)]
    prompt = diy_rag_mod.PROMPT.format(
        context="\n\n".join(f"[{h['source']}]\n{h['text']}" for h, _ in hits),
        question="R²は？",
    )
    assert "R² = 0.488" in prompt
    assert "R²は？" in prompt
    assert "資料にありません" in prompt
