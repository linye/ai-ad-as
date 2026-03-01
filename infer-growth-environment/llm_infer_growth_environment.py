#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Infer the preferred growth environment of microbial genera using OpenAI LLM.

Usage
-----
python llm_infer_growth_environment.py \
    --input genera.txt \
    --output output.tsv \
    [--model gpt-4o] \
    [--sleep 0.2]

Arguments
---------
--input   Path to input file (one genus name per line)
--output  Path to output TSV file
--model   OpenAI model name (default: gpt-4o)
--sleep   Sleep time (seconds) between API calls (default: 0.2)

Requirements
------------
- Python >= 3.8
- openai >= 1.0.0

Before running this script:
1. Install dependencies:
   pip install -U openai

2. Configure OpenAI API key (one of the following):
   - Environment variable (recommended):
       export OPENAI_API_KEY="YOUR_API_KEY"
   - Or modify the code to pass api_key explicitly

Output format
-------------
genus    preferred_growth_environment    description_of_characteristics
"""

import json
import os
import time
import re
import argparse
from typing import Dict, Any

from openai import OpenAI


# -----------------------------
# Utility functions
# -----------------------------
def build_prompt(genus: str) -> str:
    """
    Build a prompt that explicitly requires valid JSON output.

    IMPORTANT:
    - Use double quotes in JSON examples
    - Do NOT include any extra text outside JSON
    """
    return f"""
You are a microbiologist specializing in wastewater treatment microbiomes.

Given the bacterial genus "{genus}", summarize its key characteristics
(e.g., metabolism, oxygen tolerance, typical habitats), and infer whether
it prefers growth in:
- aerobic activated sludge systems (AS),
- anaerobic digestion systems (AD),
- both (BOTH),
- or if the evidence is insufficient (UNSURE).

Return ONLY a valid JSON object with the following structure
(using double quotes, no comments, no extra text):

{{
  "description_of_characteristics": "concise scientific description",
  "preferred_growth_environment": "AS | AD | BOTH | UNSURE"
}}
"""


def extract_json(text: str) -> Dict[str, Any]:
    """
    Extract and parse the first JSON object from model output.

    This function is intentionally conservative and does NOT
    change the JSON structure defined by the original script.
    """
    # Remove Markdown code fences if present
    text = re.sub(r"```json|```", "", text, flags=re.IGNORECASE).strip()

    # Extract the first {...} block
    match = re.search(r"\{.*\}", text, flags=re.DOTALL)
    if not match:
        raise ValueError("No JSON object found in model output")

    json_str = match.group(0)

    # Parse JSON strictly
    return json.loads(json_str)


# -----------------------------
# Main function
# -----------------------------
def main():
    parser = argparse.ArgumentParser(
        description="Infer preferred growth environment (AS/AD/BOTH/UNSURE) for microbial genera using OpenAI."
    )
    parser.add_argument("--input", required=True, help="Input file (one genus per line)")
    parser.add_argument("--output", required=True, help="Output TSV file")
    parser.add_argument("--model", default="gpt-4o", help="OpenAI model name (default: gpt-4o)")
    parser.add_argument("--sleep", type=float, default=0.2, help="Sleep time between API calls (seconds)")

    args = parser.parse_args()

    if not os.path.exists(args.input):
        raise FileNotFoundError(f"Input file not found: {args.input}")

    # Initialize OpenAI client (API key is read from environment variable)
    client = OpenAI()

    with open(args.input, "r", encoding="utf-8") as fin, \
         open(args.output, "a", encoding="utf-8") as fout:

        for line in fin:
            genus = line.strip()
            if not genus:
                continue

            try:
                response = client.chat.completions.create(
                    model=args.model,
                    messages=[
                        {"role": "system", "content": "You are a scientific assistant."},
                        {"role": "user", "content": build_prompt(genus)},
                    ],
                    temperature=0.2,
                )

                raw_text = response.choices[0].message.content
                data = extract_json(raw_text)

                fout.write(
                    f"{genus}\t"
                    f"{data['preferred_growth_environment']}\t"
                    f"{data['description_of_characteristics']}\n"
                )
                fout.flush()

                print(f"[OK] {genus} -> {data['preferred_growth_environment']}")

            except Exception as e:
                # Do not stop the whole pipeline if one genus fails
                fout.write(f"{genus}\tERROR\t{str(e)}\n")
                fout.flush()
                print(f"[ERROR] {genus}: {e}")

            time.sleep(args.sleep)


if __name__ == "__main__":
    main()