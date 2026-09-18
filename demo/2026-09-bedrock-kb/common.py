"""デモ共通の設定とヘルパー。

AWS が使えない環境（鍵なし・オフライン）でも同じ出力が出るよう、
実行結果のスナップショットへフォールバックする。
demo/_shared/reinfolib.py と同じ考え方。
"""

import json
import os
from pathlib import Path

DEMO_DIR = Path(__file__).resolve().parent
SNAPSHOT_DIR = DEMO_DIR / "snapshots"
SLIDES_DIR = DEMO_DIR.parent.parent / "slides"

REGION = os.environ.get("AWS_REGION", "ap-northeast-1")

# 推論プロファイル経由で呼ぶ。素の "anthropic.claude-..." を渡すと
# ValidationException になる（スライドで触れるハマりどころ）。
CHAT_MODEL_ID = os.environ.get("BEDROCK_CHAT_MODEL", "jp.anthropic.claude-haiku-4-5-20251001-v1:0")
EMBED_MODEL_ID = os.environ.get("BEDROCK_EMBED_MODEL", "amazon.titan-embed-text-v2:0")

# provision.sh が出力する Knowledge Base ID を環境変数で受け取る
KNOWLEDGE_BASE_ID = os.environ.get("KNOWLEDGE_BASE_ID", "")

# 発表で使う質問。4本のスライドのうち Part2（回帰分析）にだけ答えがある
QUESTION = "飛騨高山Pythonの会の不動産データ分析で、重回帰分析の決定係数R²はいくつでしたか？"

# 資料に含めないスライド。この回の発表資料そのものを入れると、
# 答えがスライドに書いてあるため検索のデモにならない。
EXCLUDED_SLIDES = {"2026-09-bedrock-kb"}


def load_snapshot(name):
    """スナップショットを読む。無ければ None。"""
    path = SNAPSHOT_DIR / f"{name}.json"
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def save_snapshot(name, data):
    """実行結果をスナップショットとして保存する。"""
    SNAPSHOT_DIR.mkdir(exist_ok=True)
    path = SNAPSHOT_DIR / f"{name}.json"
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return path


def account_id():
    """実行中のアカウントID。環境変数が無ければ STS から引く。"""
    cached = os.environ.get("AWS_ACCOUNT_ID")
    if cached:
        return cached
    import boto3

    resolved = boto3.client("sts", region_name=REGION).get_caller_identity()["Account"]
    os.environ["AWS_ACCOUNT_ID"] = resolved
    return resolved


def bedrock_runtime():
    import boto3

    return boto3.client("bedrock-runtime", region_name=REGION)


def agent_runtime():
    import boto3

    return boto3.client("bedrock-agent-runtime", region_name=REGION)


def ask_claude(client, prompt, max_tokens=512):
    """Converse API で Claude に一往復だけ聞く。"""
    response = client.converse(
        modelId=CHAT_MODEL_ID,
        messages=[{"role": "user", "content": [{"text": prompt}]}],
        inferenceConfig={"maxTokens": max_tokens, "temperature": 0},
    )
    return response["output"]["message"]["content"][0]["text"]


def banner(title):
    print()
    print("=" * 70)
    print(title)
    print("=" * 70)
