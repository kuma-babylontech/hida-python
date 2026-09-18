"""③ RetrieveAndGenerate — 検索と生成をまとめて1回で。

② の Retrieve に「回答の生成」まで含めたもの。
返り値には回答文と citations（どのチャンクを根拠にしたか）が入る。

出典は LLM に書かせず、citations から機械的に組み立てる。
LLM に書かせると、資料に無い出典を創作する余地が残るため。
"""

import os

import common


def model_arn():
    """推論プロファイルの ARN を組み立てる。

    素のモデルID を渡すと ValidationException になるため、
    `jp.` 付きのプロファイルを ARN の形で指定する。
    """
    override = os.environ.get("BEDROCK_MODEL_ARN")
    if override:
        return override
    return f"arn:aws:bedrock:{common.REGION}:{common.account_id()}:inference-profile/{common.CHAT_MODEL_ID}"


def retrieve_and_generate(question):
    client = common.agent_runtime()
    return client.retrieve_and_generate(
        input={"text": question},
        retrieveAndGenerateConfiguration={
            "type": "KNOWLEDGE_BASE",
            "knowledgeBaseConfiguration": {
                "knowledgeBaseId": common.KNOWLEDGE_BASE_ID,
                "modelArn": model_arn(),
            },
        },
    )


def build_citations(response):
    """citations から出典の一覧を作る。LLM の文章からは作らない。"""
    sources = []
    for citation in response.get("citations", []):
        for reference in citation.get("retrievedReferences", []):
            uri = reference["location"]["s3Location"]["uri"]
            sources.append(
                {
                    "document": uri.split("/")[-1],
                    "excerpt": reference["content"]["text"][:120].replace("\n", " "),
                }
            )
    return sources


def main():
    common.banner("③ RetrieveAndGenerate — 検索＋生成を1回で")
    print(f"質問: {common.QUESTION}")
    print()

    try:
        response = retrieve_and_generate(common.QUESTION)
        answer = response["output"]["text"]
        sources = build_citations(response)
        common.save_snapshot(
            "03_retrieve_and_generate",
            {"question": common.QUESTION, "answer": answer, "sources": sources},
        )
    except Exception as exc:
        snapshot = common.load_snapshot("03_retrieve_and_generate")
        if snapshot is None:
            raise
        print(f"[AWS を呼べないためスナップショットを使用: {type(exc).__name__}]")
        answer = snapshot["answer"]
        sources = snapshot["sources"]

    print("回答:")
    print(answer)
    print()
    print("出典（citations から機械的に組み立て）:")
    for i, source in enumerate(sources, 1):
        print(f"  [{i}] {source['document']}")
        print(f"      {source['excerpt']}")
    print()
    print("→ ここまでで書いた『RAGのコード』は 0 行。全部 Knowledge Bases 任せ。")


if __name__ == "__main__":
    main()
