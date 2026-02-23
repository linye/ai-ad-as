# AI-AD-AS Project

This project provides a machine learning framework for predicting bacterial preferred growth environments—activated sludge (AS) or anaerobic digestion (AD)—based on 16S rRNA gene sequences.

---

## 1. Model Construction

The machine learning model for predicting AS- and AD-associated bacteria from 16S rRNA gene sequences can be constructed following the procedures provided in the Jupyter notebooks located in the `model-construction` directory. The notebook includes: Data preprocessing, DNA sequence encoding, Model training and Performance evaluation.

The dataset file (dataset.csv.gz) should be decompressed prior to model construction.

---

## 2. Model Application

A pretrained model is provided in the `model-application` directory and can be used to predict bacterial growth environment categories (AS, AD, BOTH, UNSURE) from 16S rRNA gene sequences by following the steps below.

---

### 2.1 Software Requirements

- Python ≥ 3.9  
- scikit-learn == 1.4.2 *(other versions are not supported)*  
- joblib  
- biopython  

---

### 2.2 Installation

Install the required Python packages using:

```bash
pip install scikit-learn==1.4.2 joblib biopython
```

---

### 2.3 Prediction Workflow

- Prepare your 16S rRNA gene sequences in FASTA format and name the file `input.fa`.
- Run the prediction script:
   ```bash
   python predict-ASAD.py
   ```
- Prediction results will be saved to `output.csv`.

---

### 2.4 Notes and Limitations

**Training label source**  
Training labels (AS, AD, BOTH, UNSURE) were generated using the ChatGPT API.

**Sequence length consideration**  
The model was trained on near full-length 16S rRNA gene sequences from the MiDAS database. Predictions based on shorter sequences (<1300 bp) may show reduced reliability.
