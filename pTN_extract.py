import json
from typing import List
import pandas as pd
from pydantic import BaseModel
from openai import OpenAI
import argparse

class TNMClassification(BaseModel):
    T: str
    N: str

    def __str__(self):
        return str({'T': self.T, 'N': self.N})

def read_prompt(prompt_file: str) -> str:
    with open(prompt_file, 'r', encoding='utf-8') as f:
        return f.read().strip()

def process_report(report: str, prompt: str, model_name: str) -> str:
    client = OpenAI(
        api_key="your-endpoint-api-key",
        base_url="your-endpoint-base-url"
    )
    
    print(f"Request details:")
    print(f"Model: {model_name}")
    print(f"Report: {report[:100]}...")
    
    combined_prompt = f"{prompt}\n\nreport:\n{report}"
    
    try:
        response = client.beta.chat.completions.parse(
            model=model_name,
            messages=[
                {"role": "user", "content": combined_prompt}
            ],
            temperature=0, 
            max_tokens=2048,
            response_format=TNMClassification,
        )
        
        extracted_text = response.choices[0].message.parsed
        print(f"LLM response: {extracted_text}")
        return extracted_text
            
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return "[]"

def main():
    parser = argparse.ArgumentParser(description='Script to extract information from medical reports')
    parser.add_argument('--model', type=str, default='Qwen/Qwen2.5-72B-Instruct-GPTQ-Int4',
                      help='Model name to use (default: Qwen/Qwen2.5-72B-Instruct-GPTQ-Int4)')
    parser.add_argument('--prompt', type=str, default='prompts/pTN_prompt_english.txt',
                      help='Path to prompt file (default: prompts/pTN_prompt_english.txt)')
    parser.add_argument('--input', type=str, default='data/input.csv',
                      help='Path to input CSV file (default: data/input.csv)')
    args = parser.parse_args()
    
    prompt = read_prompt(args.prompt)
    
    print(f"Loading CSV file: {args.input}")
    df = pd.read_csv(
        args.input,
        encoding='utf-8'
    )
    print(f"Data shape: {df.shape}")
    print("Column names:", df.columns.tolist())
    
    print("\nFirst row data:")
    print(df.iloc[0])
    
    results = []
    
    for idx, row in df.iterrows():
        print(f"\nProcessing ID: {row['ID'] if 'ID' in row else 'unknown'}")
        try:
            result = {
                'id': str(row['ID']),
                'tn_info': process_report(row['report'], prompt, args.model)
            }
            results.append(result)
        except Exception as e:
            print(f"Error processing ID {row['ID'] if 'ID' in row else idx}: {str(e)}")
            continue
    
    if not results:
        print("Warning: No results were processed")
        return
        
    final_df = pd.DataFrame(results)
    final_df.to_csv('output.csv', index=False, encoding='utf-8')

if __name__ == '__main__':
    main() 