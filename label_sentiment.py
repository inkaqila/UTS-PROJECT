# label_sentiment.py

import pandas as pd
from transformers import pipeline

def label_sentiment(input_csv="dataset_clean.csv",
                    output_csv="dataset_label.csv"):
    # 1. Load data
    df = pd.read_csv(input_csv)
    if 'komentar' not in df.columns:
        raise ValueError("Kolom 'komentar' tidak ditemukan!")

    # 2. Inisialisasi pipeline
    classifier = pipeline(
        "sentiment-analysis",
        model="w11wo/indonesian-roberta-base-sentiment-classifier",
        tokenizer="w11wo/indonesian-roberta-base-sentiment-classifier"
    )

    # 3. Fungsi mapping ke label Indonesia
    def map_label(res):
        lbl = res['label']
        # Model SmSA punya tiga label: “LABEL_0”, “LABEL_1”, “LABEL_2”
        # Cek mapping sebenarnya dengan: classifier.model.config.id2label
        mapping = {
            "LABEL_0": "Negatif",
            "LABEL_1": "Netral",
            "LABEL_2": "Positif"
        }
        return mapping.get(lbl, lbl)

    # 4. Terapkan ke setiap komentar
    sentiments = []
    for text in df['komentar'].astype(str).tolist():
        out = classifier(text[:512])[0]  # potong maksimal 512 token
        sentiments.append(map_label(out))

    df['sentimen'] = sentiments

    # 5. Simpan hasil
    df.to_csv(output_csv, index=False, encoding="utf-8")
    print(f"✅ Hasil labeling disimpan ke {output_csv}")
    print(df[['komentar','sentimen']].head())

if __name__ == "__main__":
    label_sentiment()
