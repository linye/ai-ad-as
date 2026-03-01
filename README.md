# AI-AD-AS Project

This project provides a machine learning framework for predicting bacterial preferred growth environments—activated sludge (AS) or anaerobic digestion (AD)—based on 16S rRNA gene sequences.

---

## 1. Growth Environment Inference

An LLM–based script for inferring the preferred growth environment of microbial genera directly from taxonomic names.

---

### 1.1 Software Requirements

- Python ≥ 3.9  
- openai ≥ 1.0.0

---

### 1.2 API Configuration

Before running the script, an OpenAI API key must be configured. The recommended approach is to set it as an environment variable:

```bash
export OPENAI_API_KEY="YOUR_API_KEY"
```

---

### 1.3 Usage

Prepare a plain text file containing one genus name per line (e.g., genera.txt). Then run:

```bash
python llm_infer_growth_environment.py \
  --input genera.txt \
  --output llm_output.tsv \
  --model gpt-4o \
```

**Arguments** 

```bash
--input Input file with one genus name per line
--output Output TSV file containing inference results
--model OpenAI model name (default: gpt-4o)
```

---

## 2. Model Construction

The machine learning model for predicting AS- and AD-associated bacteria from 16S rRNA gene sequences can be constructed following the procedures provided in the Jupyter notebooks located in the `model-construction` directory. The notebook includes: Data preprocessing, DNA sequence encoding, Model training and Performance evaluation.

The dataset file (dataset.csv.gz) should be decompressed prior to model construction.

---

## 3. Model Application

A pretrained model is provided in the `model-application` directory and can be used to predict bacterial growth environment categories (AS, AD, BOTH, UNSURE) from 16S rRNA gene sequences by following the steps below.

---

### 3.1 Software Requirements

- Python ≥ 3.9  
- scikit-learn == 1.4.2 *(other versions are not supported)*  
- joblib  
- biopython  

---

### 3.2 Installation

Install the required Python packages using:

```bash
pip install scikit-learn==1.4.2 joblib biopython
```

---

### 3.3 Prediction Workflow

- Prepare your 16S rRNA gene sequences in FASTA format and name the file `input.fa`.
- Run the prediction script:
   ```bash
   python predict-ASAD.py
   ```
- Prediction results will be saved to `output.csv`.

---

### 3.4 Notes and Limitations

**Training label source**  
Training labels (AS, AD, BOTH, UNSURE) were generated using the ChatGPT API.

**Sequence length consideration**  
The model was trained on near full-length 16S rRNA gene sequences from the MiDAS database. Predictions based on shorter sequences (<1300 bp) may show reduced reliability.
