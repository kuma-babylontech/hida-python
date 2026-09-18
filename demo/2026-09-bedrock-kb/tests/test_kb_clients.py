"""Knowledge Bases 側の、AWS を呼ばない部分のテスト。

返ってきた JSON から出典を組み立てる処理は純粋な関数なので、
ダミーの応答でテストできる。出典を落とさないことがここでの関心事。
"""


def test_summarize_extracts_citation_fields(kb_retrieve_mod):
    results = [
        {
            "score": 0.51264,
            "location": {"s3Location": {"uri": "s3://bucket/slides/2026-06-real-estate-regression.md"}},
            "content": {"text": "重回帰の\nR² = 0.488"},
        }
    ]

    rows = kb_retrieve_mod.summarize(results)

    assert rows[0]["score"] == 0.5126
    assert rows[0]["source"].endswith("2026-06-real-estate-regression.md")
    assert "\n" not in rows[0]["excerpt"]


def test_build_citations_collects_every_reference(kb_rag_mod):
    response = {
        "citations": [
            {
                "retrievedReferences": [
                    {
                        "location": {"s3Location": {"uri": "s3://bucket/slides/a.md"}},
                        "content": {"text": "本文A"},
                    },
                    {
                        "location": {"s3Location": {"uri": "s3://bucket/slides/b.md"}},
                        "content": {"text": "本文B"},
                    },
                ]
            }
        ]
    }

    sources = kb_rag_mod.build_citations(response)

    assert [s["document"] for s in sources] == ["a.md", "b.md"]


def test_build_citations_without_references_is_empty(kb_rag_mod):
    assert kb_rag_mod.build_citations({"citations": [{"retrievedReferences": []}]}) == []


def test_model_arn_points_at_inference_profile(kb_rag_mod, common_mod, monkeypatch):
    # STS を呼ばせないためアカウントIDを与える
    monkeypatch.setenv("AWS_ACCOUNT_ID", "000000000000")
    monkeypatch.delenv("BEDROCK_MODEL_ARN", raising=False)

    arn = kb_rag_mod.model_arn()

    assert ":inference-profile/" in arn
    assert arn.endswith(common_mod.CHAT_MODEL_ID)


def test_model_arn_can_be_overridden(kb_rag_mod, monkeypatch):
    monkeypatch.setenv("BEDROCK_MODEL_ARN", "arn:aws:bedrock:us-east-1::foundation-model/x")
    assert kb_rag_mod.model_arn().endswith("foundation-model/x")
