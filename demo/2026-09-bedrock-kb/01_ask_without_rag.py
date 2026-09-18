"""① RAG なしで聞いてみる。

Bedrock の Claude にそのまま質問する。
学習データに無い「この勉強会の過去の発表内容」は答えられない。
ここが RAG の出発点。
"""

import common


def main():
    common.banner("① RAG なし — Claude にそのまま聞く")
    print(f"質問: {common.QUESTION}")
    print()

    try:
        answer = common.ask_claude(common.bedrock_runtime(), common.QUESTION)
        common.save_snapshot("01_without_rag", {"question": common.QUESTION, "answer": answer})
    except Exception as exc:  # 鍵なし・オフライン時はスナップショットへ
        snapshot = common.load_snapshot("01_without_rag")
        if snapshot is None:
            raise
        print(f"[AWS を呼べないためスナップショットを使用: {type(exc).__name__}]")
        answer = snapshot["answer"]

    print("回答:")
    print(answer)
    print()
    print("→ 資料を渡していないので、答えようがない。")
    print("  ファインチューニングではなく『検索して渡す』のが RAG。")


if __name__ == "__main__":
    main()
