#!/usr/bin/env bash
# Bedrock Knowledge Bases のデモ環境を作る。
#
#   AWS_PROFILE=babylon-tech ./setup/provision.sh
#
# 最後に出る KNOWLEDGE_BASE_ID を export してから 02/03 のスクリプトを動かす。
# 片付けは ./setup/teardown.sh。
set -euo pipefail

REGION="${AWS_REGION:-ap-northeast-1}"
ACCOUNT_ID="${AWS_ACCOUNT_ID:-$(aws sts get-caller-identity --query Account --output text)}"
DOC_BUCKET="hida-python-kb-demo-${ACCOUNT_ID}"
VECTOR_BUCKET="hida-python-kb-demo"
INDEX_NAME="slides-index"
ROLE_NAME="HidaPythonKBDemoRole"
KB_NAME="hida-python-slides"
EMBED_MODEL="arn:aws:bedrock:${REGION}::foundation-model/amazon.titan-embed-text-v2:0"

SETUP_DIR="$(cd "$(dirname "$0")" && pwd)"
DEMO_DIR="$(dirname "$SETUP_DIR")"
SLIDES_DIR="$(cd "$DEMO_DIR/../../slides" && pwd)"

export AWS_REGION="$REGION"

echo "==> 1/6 資料用 S3 バケット"
aws s3api head-bucket --bucket "$DOC_BUCKET" 2>/dev/null || \
  aws s3api create-bucket --bucket "$DOC_BUCKET" --region "$REGION" \
    --create-bucket-configuration "LocationConstraint=${REGION}" >/dev/null
aws s3api put-public-access-block --bucket "$DOC_BUCKET" \
  --public-access-block-configuration \
  BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true

echo "==> 2/6 スライドをアップロード（この回の発表資料そのものは除く）"
find "$SLIDES_DIR" -name slide.md -print0 | while IFS= read -r -d '' path; do
  name="$(basename "$(dirname "$path")")"
  if [ "$name" = "2026-09-bedrock-kb" ]; then
    continue
  fi
  aws s3 cp "$path" "s3://${DOC_BUCKET}/slides/${name}.md" --only-show-errors
done

echo "==> 3/6 S3 Vectors バケットとインデックス（1024次元 / cosine）"
aws s3vectors get-vector-bucket --vector-bucket-name "$VECTOR_BUCKET" >/dev/null 2>&1 || \
  aws s3vectors create-vector-bucket --vector-bucket-name "$VECTOR_BUCKET" >/dev/null
aws s3vectors get-index --vector-bucket-name "$VECTOR_BUCKET" --index-name "$INDEX_NAME" >/dev/null 2>&1 || \
  aws s3vectors create-index --vector-bucket-name "$VECTOR_BUCKET" --index-name "$INDEX_NAME" \
    --data-type float32 --dimension 1024 --distance-metric cosine \
    --metadata-configuration '{"nonFilterableMetadataKeys":["AMAZON_BEDROCK_TEXT"]}' >/dev/null

echo "==> 4/6 Knowledge Bases 用の IAM ロール"
# ポリシーはアカウントIDを埋め込んでから渡す（リポジトリには直書きしない）
WORK_DIR="$(mktemp -d)"
trap 'rm -rf "$WORK_DIR"' EXIT
sed -e "s/__ACCOUNT_ID__/${ACCOUNT_ID}/g" -e "s/__REGION__/${REGION}/g" \
  "${SETUP_DIR}/trust-policy.json" > "${WORK_DIR}/trust-policy.json"
sed -e "s/__ACCOUNT_ID__/${ACCOUNT_ID}/g" -e "s/__REGION__/${REGION}/g" \
  "${SETUP_DIR}/role-policy.json" > "${WORK_DIR}/role-policy.json"

if ! aws iam get-role --role-name "$ROLE_NAME" >/dev/null 2>&1; then
  aws iam create-role --role-name "$ROLE_NAME" \
    --assume-role-policy-document "file://${WORK_DIR}/trust-policy.json" \
    --description "Hida Takayama Python meetup #80 Bedrock KB demo" >/dev/null
  echo "    ロールの反映を待つ (15s)"
  sleep 15
fi
aws iam put-role-policy --role-name "$ROLE_NAME" --policy-name KBDemoAccess \
  --policy-document "file://${WORK_DIR}/role-policy.json"
ROLE_ARN="arn:aws:iam::${ACCOUNT_ID}:role/${ROLE_NAME}"

echo "==> 5/6 Knowledge Base とデータソース"
KB_ID="$(aws bedrock-agent list-knowledge-bases \
  --query "knowledgeBaseSummaries[?name=='${KB_NAME}'].knowledgeBaseId | [0]" --output text)"
if [ "$KB_ID" = "None" ] || [ -z "$KB_ID" ]; then
  KB_ID="$(aws bedrock-agent create-knowledge-base \
    --name "$KB_NAME" \
    --role-arn "$ROLE_ARN" \
    --knowledge-base-configuration "{\"type\":\"VECTOR\",\"vectorKnowledgeBaseConfiguration\":{\"embeddingModelArn\":\"${EMBED_MODEL}\"}}" \
    --storage-configuration "{\"type\":\"S3_VECTORS\",\"s3VectorsConfiguration\":{\"indexArn\":\"arn:aws:s3vectors:${REGION}:${ACCOUNT_ID}:bucket/${VECTOR_BUCKET}/index/${INDEX_NAME}\"}}" \
    --query 'knowledgeBase.knowledgeBaseId' --output text)"
fi

DS_ID="$(aws bedrock-agent list-data-sources --knowledge-base-id "$KB_ID" \
  --query "dataSourceSummaries[0].dataSourceId | [0]" --output text 2>/dev/null || echo None)"
if [ "$DS_ID" = "None" ] || [ -z "$DS_ID" ]; then
  DS_ID="$(aws bedrock-agent create-data-source \
    --knowledge-base-id "$KB_ID" --name slides \
    --data-source-configuration "{\"type\":\"S3\",\"s3Configuration\":{\"bucketArn\":\"arn:aws:s3:::${DOC_BUCKET}\",\"inclusionPrefixes\":[\"slides/\"]}}" \
    --query 'dataSource.dataSourceId' --output text)"
fi

echo "==> 6/6 同期（ingestion job）"
JOB_ID="$(aws bedrock-agent start-ingestion-job --knowledge-base-id "$KB_ID" \
  --data-source-id "$DS_ID" --query 'ingestionJob.ingestionJobId' --output text)"
while true; do
  STATUS="$(aws bedrock-agent get-ingestion-job --knowledge-base-id "$KB_ID" \
    --data-source-id "$DS_ID" --ingestion-job-id "$JOB_ID" \
    --query 'ingestionJob.status' --output text)"
  echo "    status=${STATUS}"
  case "$STATUS" in
    COMPLETE) break ;;
    FAILED) echo "同期に失敗した。get-ingestion-job で詳細を確認する。"; exit 1 ;;
  esac
  sleep 10
done

echo
echo "完了。次のコマンドで 02/03 が動く:"
echo "  export KNOWLEDGE_BASE_ID=${KB_ID}"
