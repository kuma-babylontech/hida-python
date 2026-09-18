"""⑤ 任せる版と自前版を並べる。

同じ質問を Knowledge Bases（③）と自前RAG（④）に投げて、
回答と出典を横に並べる。発表の締めに使う。

KNOWLEDGE_BASE_ID が無いときは自前版だけを出す。
"""

import importlib.util
import sys
from pathlib import Path

import common


def _load(module_name, filename):
    spec = importlib.util.spec_from_file_location(module_name, Path(__file__).parent / filename)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def kb_answer():
    """Knowledge Bases 版。使えなければ None。"""
    if not common.KNOWLEDGE_BASE_ID:
        return None
    rag_module = _load("kb_rag", "03_kb_retrieve_and_generate.py")
    try:
        response = rag_module.retrieve_and_generate(common.QUESTION)
        return {
            "answer": response["output"]["text"],
            "sources": [s["document"] for s in rag_module.build_citations(response)],
        }
    except Exception:
        snapshot = common.load_snapshot("03_retrieve_and_generate")
        if snapshot is None:
            return None
        return {"answer": snapshot["answer"], "sources": [s["document"] for s in snapshot["sources"]]}


def diy_answer():
    """自前RAG 版。"""
    diy_module = _load("diy_rag", "04_diy_rag.py")
    chunks = diy_module.split_into_chunks(diy_module.load_documents())
    cache = common.load_snapshot("04_diy_rag")
    try:
        import numpy as np

        chunk_vectors = diy_module.embed_all(chunks)
        question_vector = np.array(
            diy_module.embed(common.bedrock_runtime(), common.QUESTION), dtype=np.float32
        )
        hits = diy_module.search(question_vector, chunk_vectors, chunks)
        return {
            "answer": diy_module.generate(hits, common.QUESTION),
            "sources": [h["source"] for h, _ in hits],
        }
    except Exception:
        if cache is None:
            raise
        return {"answer": cache["answer"], "sources": [h["source"] for h in cache["hits"]]}


def show(title, result):
    print(f"--- {title} ---")
    if result is None:
        print("（未構築のためスキップ。setup/provision.sh を実行して KNOWLEDGE_BASE_ID を設定する）\n")
        return
    print(result["answer"].strip())
    print(f"出典: {', '.join(dict.fromkeys(result['sources']))}\n")


def main():
    common.banner("⑤ 任せる vs 自分で書く")
    print(f"質問: {common.QUESTION}\n")
    show("③ Knowledge Bases（コード0行）", kb_answer())
    show("④ 自前RAG（約100行）", diy_answer())
    print("→ 同じ答えにたどり着く。違うのは『途中に手を入れられるか』。")


if __name__ == "__main__":
    main()
