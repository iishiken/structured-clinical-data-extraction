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

### LLM Server Configuration

This project assumes the use of the following endpoints:

1. vLLM Local Server:
```python
base_url="http://localhost:8000/v1"
```
For vLLM server configuration and startup instructions, please refer to the [vLLM official documentation](https://docs.vllm.ai/).

2. Google Gemini API:
```python
base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
```
To use Gemini, you need a Google Cloud API key. Set it as an environment variable:
```bash
export GOOGLE_API_KEY="your-api-key"
```


別のエンドポイントを使用する場合は、`pTN_extract.py`の設定を適宜変更してください。

## Project Structure

```
.
├── pTN_extract.py      # Script for pTN classification extraction
├── cM_assessment.py    # Script for cM classification assessment
├── requirements.txt    # Package dependencies
├── data/              # Data directory
│   └── input.csv      # Input data example
├── output.csv         # Output results
└── prompts/           # Prompt files directory
    ├── pTN_prompt_english.txt    # Prompt for pTN classification extraction (English)
    ├── pTN_prompt_japanease.txt  # Prompt for pTN classification extraction (Japanese)
    ├── cM_prompt_english.txt     # Prompt for cM assessment (English)
    └── cM_prompt_japanease.txt   # Prompt for cM assessment (Japanese)
```

## Usage

1. Place input CSV file in the `data/` directory
   - Required columns: `ID`, `report`
   - Encoding: UTF-8

2. Place prompt files in the `prompts/` directory
   - English prompts: `prompts/pTN_prompt_english.txt`, `prompts/cM_prompt_english.txt`
   - Japanese prompts: `prompts/pTN_prompt_japanease.txt`, `prompts/cM_prompt_japanease.txt`

3. Run the script:
```bash
# Specify model name and prompt file to run
python pTN_extract.py --model "Qwen/Qwen2.5-72B-Instruct-GPTQ-Int4" --prompt "prompts/pTN_prompt_english.txt"
python pTN_extract.py --model "gemini-1.5-pro-001" --prompt "prompts/pTN_prompt_english.txt"

python cM_assessment.py --model "Qwen/Qwen2.5-72B-Instruct-GPTQ-Int4" --prompt "prompts/cM_prompt_english.txt"
python cM_assessment.py --model "gemini-1.5-pro-001" --prompt "prompts/cM_prompt_english.txt"

```

### Models Used in the Paper

The following models were evaluated (all downloaded from Hugging Face):

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
All these models were downloaded and used from the [Hugging Face](https://huggingface.co/).

### Command Line Arguments

- `--model`: Model name to use (default: Qwen/Qwen2.5-72B-Instruct-GPTQ-Int4)
- `--prompt`: Path to prompt file (default: prompts/sample_prompt.txt)
- `--input`: Path to input CSV file (default: data/input.csv)

## Input Data Format

The input CSV file (`data/input.csv`) must be in the following format:

```csv
ID,report
1,"Report text..."
2,"Report text..."
```

## 出力

The structured TNM classification data is output as `output.csv`. Each record is saved in the following format:

```csv
id,tn_info
1,"[{"T": "pT2", "N": "pN1"}]"
2,"[{"T": "pT3", "N": "pN0"}]"
```

- `id`: Input data ID
- `tn_info`: JSON formatted string containing T and N classification or M classification information

## Prompts

The `prompts/` directory contains the following prompts used in the paper:

### Prompts for pTN Classification Extraction
- `pTN_prompt_english.txt`: English prompt for extracting pathological TNM classification
- `pTN_prompt_japanease.txt`: Japanese prompt for extracting pathological TNM classification

### Prompts for cM Assessment
- `cM_prompt_english.txt`: English prompt for assessing clinical distant metastasis (cM)
- `cM_prompt_japanease.txt`: Japanese prompt for assessing clinical distant metastasis (cM)

These prompts are optimized for extracting and assessing TNM classification from pathology reports.
