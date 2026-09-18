# Amazon Bedrock Knowledge Bases デモ（2026年9月 / 飛騨高山Pythonの会 #80）

この会の**過去の発表スライド4本**（`slides/*/slide.md`）を資料として取り込み、
自然文で質問できるようにする。同じことを次の2通りで作って比べる。

- **Knowledge Bases に任せる** — 取り込み・分割・埋め込み・検索は AWS 側。RAG のコードは0行
- **自分で書く** — 同じ4工程を boto3 と numpy だけで書く。約100行

## スクリプト

| ファイル | 内容 | AWS |
| --- | --- | --- |
| `01_ask_without_rag.py` | RAG なしで Claude に聞く（答えられない） | Bedrock のみ |
| `02_kb_retrieve.py` | `Retrieve` で検索だけする。返る JSON を見る | KB が必要 |
| `03_kb_retrieve_and_generate.py` | `RetrieveAndGenerate` で回答＋出典 | KB が必要 |
| `04_diy_rag.py` | 自前RAG（取り込み→分割→埋め込み→検索→生成） | Bedrock のみ |
| `05_compare.py` | ③と④を並べる | 片方だけでも動く |

## 動かす

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt

export AWS_PROFILE=babylon-tech
export AWS_REGION=ap-northeast-1

.venv/bin/python 01_ask_without_rag.py   # ここまでは KB 不要
.venv/bin/python 04_diy_rag.py
```

`02` / `03` には Knowledge Base が要る。

```bash
./setup/provision.sh            # S3 → S3 Vectors → IAM ロール → KB → 同期
export KNOWLEDGE_BASE_ID=XXXXXXXXXX   # provision.sh が最後に表示する
.venv/bin/python 02_kb_retrieve.py
.venv/bin/python 03_kb_retrieve_and_generate.py
```

**発表が終わったら片付ける。** S3 Vectors は保管量で課金される。

```bash
./setup/teardown.sh
```

## AWS を使わずに動かす

各スクリプトは AWS を呼べないとき `snapshots/*.json`（実行結果の記録）に切り替える。
鍵が無い環境・オフラインでも同じ出力が出る。`demo/_shared/reinfolib.py` と同じ考え方。

スナップショットは実行が成功するたびに上書きされる。

## 使うモデル

| 用途 | モデル |
| --- | --- |
| 回答の生成 | `jp.anthropic.claude-haiku-4-5-20251001-v1:0` |
| 埋め込み | `amazon.titan-embed-text-v2:0`（1024次元） |

**素のモデルID（`anthropic.claude-...`）を渡すと `ValidationException` になる。**
`jp.` や `apac.` の付いた**推論プロファイル**を指定する。
利用できるものは `aws bedrock list-inference-profiles` で確認する。

`03` が使う `modelArn` は推論プロファイルの ARN を組み立てている。
別アカウントで動かすときは `AWS_ACCOUNT_ID` か `BEDROCK_MODEL_ARN` を渡す。

## 作られる AWS リソース

| 種別 | 名前 |
| --- | --- |
| S3（資料） | `hida-python-kb-demo-<ACCOUNT_ID>` |
| S3 Vectors | バケット `hida-python-kb-demo` / インデックス `slides-index` |
| IAM ロール | `HidaPythonKBDemoRole` |
| Knowledge Base | `hida-python-slides` |

## テスト

AWS を呼ばない部分（分割・検索・出典の組み立て）だけをテストする。

```bash
.venv/bin/pip install pytest
.venv/bin/python -m pytest tests -q
```
