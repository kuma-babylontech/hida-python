#!/usr/bin/env bash
# デモ環境を片付ける。発表が終わったら流す（S3 Vectors は保管量で課金されるため）。
#
#   AWS_PROFILE=babylon-tech ./setup/teardown.sh
set -uo pipefail

REGION="${AWS_REGION:-ap-northeast-1}"
ACCOUNT_ID="${AWS_ACCOUNT_ID:-$(aws sts get-caller-identity --query Account --output text)}"
DOC_BUCKET="hida-python-kb-demo-${ACCOUNT_ID}"
VECTOR_BUCKET="hida-python-kb-demo"
INDEX_NAME="slides-index"
ROLE_NAME="HidaPythonKBDemoRole"
KB_NAME="hida-python-slides"

export AWS_REGION="$REGION"

KB_ID="$(aws bedrock-agent list-knowledge-bases \
  --query "knowledgeBaseSummaries[?name=='${KB_NAME}'].knowledgeBaseId | [0]" --output text)"
if [ "$KB_ID" != "None" ] && [ -n "$KB_ID" ]; then
  echo "==> Knowledge Base を削除: $KB_ID"
  aws bedrock-agent delete-knowledge-base --knowledge-base-id "$KB_ID" >/dev/null
  sleep 10
fi

echo "==> S3 Vectors を削除"
aws s3vectors delete-index --vector-bucket-name "$VECTOR_BUCKET" --index-name "$INDEX_NAME" >/dev/null 2>&1
aws s3vectors delete-vector-bucket --vector-bucket-name "$VECTOR_BUCKET" >/dev/null 2>&1

echo "==> 資料バケットを削除"
aws s3 rm "s3://${DOC_BUCKET}" --recursive --only-show-errors
aws s3api delete-bucket --bucket "$DOC_BUCKET" >/dev/null 2>&1

echo "==> IAM ロールを削除"
aws iam delete-role-policy --role-name "$ROLE_NAME" --policy-name KBDemoAccess 2>/dev/null
aws iam delete-role --role-name "$ROLE_NAME" 2>/dev/null

echo "完了。"
