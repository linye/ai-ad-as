import joblib
import os
from Bio import SeqIO

def get_kmers(sequence, k):
    if not isinstance(sequence, str) or len(sequence) < k:
        return []
    return [sequence[i:i+k] for i in range(len(sequence) - k + 1)]
def kmer_analyzer(sequence):
    return get_kmers(sequence, loaded_k)

model_dir = "model"
MODEL_FILENAME = os.path.join(model_dir, "bacteria_classifier_model.joblib")
VECTORIZER_FILENAME = os.path.join(model_dir, "kmer_vectorizer.joblib")
ENCODER_FILENAME = os.path.join(model_dir, "label_encoder.joblib")
KMER_VALUE_FILENAME = os.path.join(model_dir, "kmer_k_value.joblib") 

try:
    loaded_model = joblib.load(MODEL_FILENAME)
    loaded_vectorizer = joblib.load(VECTORIZER_FILENAME)
    loaded_encoder = joblib.load(ENCODER_FILENAME)
    loaded_k = joblib.load(KMER_VALUE_FILENAME) # kmer
except Exception as e:
    print(f"Error: {e}")
    exit()

def predict_bacteria_feature(sequence, model, vectorizer, label_encoder, loaded_k):
    try:
        sequence_vector = vectorizer.transform([sequence])
        prediction_numeric = model.predict(sequence_vector)
        prediction_label = label_encoder.inverse_transform(prediction_numeric)

        return prediction_label[0]

    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    out = open('output.csv','w')
    for seq_record in SeqIO.parse('input.fa', 'fasta'):
        des = str(seq_record.description)
        seq = str(seq_record.seq)
        predicted_label = predict_bacteria_feature(
            seq,
            loaded_model,
            loaded_vectorizer,
            loaded_encoder,
            loaded_k
        )
        print(f"SeqID: {des}, Feature: {predicted_label}")
        out.write(des+','+predicted_label+'\n')
    out.close()
