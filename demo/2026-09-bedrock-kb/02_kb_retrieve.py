"""② Knowledge Bases の Retrieve — 検索だけする。

生成はせず、質問に近いチャンクを引いてくるだけ。
返ってくる JSON に何が入っているかを見るのがこのスクリプトの目的。
score / content / location（＝出典の材料）が取れる。
"""

import common


def retrieve(question, top_k=3):
    client = common.agent_runtime()
    response = client.retrieve(
        knowledgeBaseId=common.KNOWLEDGE_BASE_ID,
        retrievalQuery={"text": question},
        retrievalConfiguration={"vectorSearchConfiguration": {"numberOfResults": top_k}},
    )
    return response["retrievalResults"]


def summarize(results):
    """出典カードの材料だけを抜き出す。"""
    rows = []
    for result in results:
        rows.append(
            {
                "score": round(result.get("score", 0.0), 4),
                "source": result["location"]["s3Location"]["uri"],
                "excerpt": result["content"]["text"][:160].replace("\n", " "),
            }
        )
    return rows


def main():
    common.banner("② Retrieve — 検索だけ（生成しない）")
    print(f"質問: {common.QUESTION}")
    print()

    try:
        results = retrieve(common.QUESTION)
        rows = summarize(results)
        common.save_snapshot("02_retrieve", {"question": common.QUESTION, "results": rows})
    except Exception as exc:
        snapshot = common.load_snapshot("02_retrieve")
        if snapshot is None:
            raise
        print(f"[AWS を呼べないためスナップショットを使用: {type(exc).__name__}]")
        rows = snapshot["results"]

    for i, row in enumerate(rows, 1):
        print(f"[{i}] score={row['score']}  出典={row['source'].split('/')[-1]}")
        print(f"    {row['excerpt']}")
        print()

    print("→ score・出典ファイル名・本文が返る。この3つで出典カードが作れる。")


if __name__ == "__main__":
    main()
