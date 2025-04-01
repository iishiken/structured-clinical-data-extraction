# Structured Clinical Data Extraction

Automatically extracts and assesses TNM classification from clinical reports using various LLMs.

## Features

- Load report data from CSV files
- Extract/assess TNM classification using prompts
- Output structured data using Pydantic
- Export results in CSV format

## Setup

Clone this repository:
```bash
git clone https://github.com/iishiken/structured-clinical-data-extraction
```
Set up a clean python3 virtual environment, i.e.
```bash
conda create -n structured-clinical-data-extraction python=3.11
conda activate structured-clinical-data-extraction
```

Install necessary dependencies. :
```bash
cd structured-clinical-data-extraction 
pip install -r requirements.txt
```

### LLMサーバーの設定

このプロジェクトでは、以下のエンドポイントを使用することを想定しています：

1. vLLMローカルサーバー:
```python
base_url="http://localhost:8000/v1"
```
vLLMサーバーの設定と起動方法については、[vLLMの公式ドキュメント](https://docs.vllm.ai/)を参照してください。

2. Google Gemini API:
```python
base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
```

Geminiを使用する場合は、Google Cloud APIキーが必要です。環境変数として設定してください：
```bash
export GOOGLE_API_KEY="your-api-key"
```


別のエンドポイントを使用する場合は、`pTN_extract.py`の設定を適宜変更してください。

## プロジェクト構造

```
.
├── pTN_extract.py      # pTN分類抽出スクリプト
├── cM_assessment.py    # cM分類判定スクリプト
├── requirements.txt    # 依存パッケージ
├── data/              # データディレクトリ
│   └── input.csv      # 入力データ例
├── output.csv         # 出力結果
└── prompts/           # プロンプトファイルディレクトリ
    ├── pTN_prompt_english.txt    # pTN分類抽出用プロンプト（英語）
    ├── pTN_prompt_japanease.txt  # pTN分類抽出用プロンプト（日本語）
    ├── cM_prompt_english.txt     # cM判定用プロンプト（英語）
    └── cM_prompt_japanease.txt   # cM判定用プロンプト（日本語）
```

## 使用方法

1. 入力CSVファイルを`data/`ディレクトリに配置
   - 必須列: `ID`, `report`
   - エンコーディング: UTF-8

2. プロンプトファイルを`prompts/`ディレクトリに配置
   - 英語版プロンプト: `prompts/pTN_prompt_english.txt`, `prompts/cM_prompt_english.txt`
   - 日本語版プロンプト: `prompts/pTN_prompt_japanease.txt`, `prompts/cM_prompt_japanease.txt`

3. スクリプトを実行:
```bash
# モデル名とプロンプトファイルを指定して実行
python pTN_extract.py --model "Qwen/Qwen2.5-72B-Instruct-GPTQ-Int4" --prompt "prompts/pTN_prompt_english.txt"
python pTN_extract.py --model "gemini-1.5-pro-001" --prompt "prompts/pTN_prompt_english.txt"

python cM_assessment.py --model "Qwen/Qwen2.5-72B-Instruct-GPTQ-Int4" --prompt "prompts/cM_prompt_english.txt"
python cM_assessment.py --model "gemini-1.5-pro-001" --prompt "prompts/cM_prompt_english.txt"

```

### 論文で使用したモデル

以下のモデルで評価を実施しています（全てHugging Faceからダウンロード）：

- Qwen family
  - `Qwen/Qwen2.5-32B-Instruct-GPTQ-Int4`
  - `Qwen/Qwen2.5-72B-Instruct-GPTQ-Int4`
  - `OPEA/QwQ-32B-int4-AutoRound-gptq-sym`

- Meta Llama family
  - `shuyuej/Llama-3.2-3B-GPTQ`
  - `hugging-quants--Meta-Llama-3.1-8B-Instruct-GPTQ-INT4`
  - `hugging-quants--Meta-Llama-3.1-70B-Instruct-GPTQ-INT4`
  - `shuyuej/Llama-3.3-70B-Instruct-GPTQ`

- Gemma family
  - `shuyuej/gemma-2-27b-it-GPTQ`

これらのモデルは全て[Hugging Face](https://huggingface.co/)のモデルハブからダウンロードして使用しています。

### コマンドライン引数

- `--model`: 使用するモデル名（デフォルト: Qwen/Qwen2.5-72B-Instruct-GPTQ-Int4）
- `--prompt`: プロンプトファイルのパス（デフォルト: prompts/sample_prompt.txt）
- `--input`: 入力CSVファイルのパス（デフォルト: data/input.csv）

## 入力データ形式

入力CSVファイル（`data/input.csv`）は以下の形式である必要があります：

```csv
ID,report
1,"病理レポート本文..."
2,"病理レポート本文..."
```

## 出力

構造化されたTNM分類データは`output.csv`として出力されます。各レコードは以下の形式で保存されます：

```csv
id,tn_info
1,"[{\"T\": \"pT2\", \"N\": \"pN1\"}]"
2,"[{\"T\": \"pT3\", \"N\": \"pN0\"}]"
```

- `id`: 入力データのID
- `tn_info`: JSON形式の文字列で、T分類とN分類もしくはM分類の情報を含む

## プロンプト

`prompts/`ディレクトリには、論文で使用した以下のプロンプトを収録しています：

### pTN分類抽出用プロンプト
- `pTN_prompt_english.txt`: 病理学的TNM分類を抽出するための英語プロンプト
- `pTN_prompt_japanease.txt`: 病理学的TNM分類を抽出するための日本語プロンプト

### cM判定用プロンプト
- `cM_prompt_english.txt`: 臨床的遠隔転移（cM）を判定するための英語プロンプト
- `cM_prompt_japanease.txt`: 臨床的遠隔転移（cM）を判定するための日本語プロンプト

これらのプロンプトは、病理レポートからTNM分類を抽出・判定するために最適化されています。
