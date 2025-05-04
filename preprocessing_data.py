import pandas as pd
from sklearn.model_selection import train_test_split
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
import pickle

def run(input_csv="dataset_label.csv",
        tokenizer_path="tokenizer.pkl",
        max_words=10000,
        max_len=100):
    # 1. Load data
    df = pd.read_csv(input_csv)
    
    # Pastikan kolom ada
    if 'komentar' not in df.columns or 'sentimen' not in df.columns:
        raise ValueError("Butuh kolom 'komentar' & 'sentimen' di CSV!")
    
    # 2. Mapping label bahasa Inggris ke Bahasa Indonesia
    map_raw = {
        'NEGATIVE': 'Negatif',
        'NEUTRAL':  'Netral',
        'POSITIVE': 'Positif',
        'LABEL_0':  'Negatif',  # jika model menggunakan label numeric
        'LABEL_1':  'Netral',
        'LABEL_2':  'Positif'
    }
    df['sentimen'] = df['sentimen'].apply(lambda x: map_raw.get(str(x).upper(), str(x)))

    # 3. Periksa dan tangani NaN di kolom 'sentimen'
    if df['sentimen'].isnull().sum() > 0:
        print(f"⚠️ Ada {df['sentimen'].isnull().sum()} baris dengan nilai NaN di kolom 'sentimen'.")
        df = df.dropna(subset=['sentimen'])  # Menghapus baris dengan NaN di 'sentimen'
        print("✅ Baris dengan NaN dihapus.")

    # 4. Periksa dan tangani NaN pada kolom 'komentar'
    if df['komentar'].isnull().sum() > 0:
        print(f"⚠️ Ada {df['komentar'].isnull().sum()} baris dengan nilai NaN di kolom 'komentar'.")
        df = df.dropna(subset=['komentar'])
        print("✅ Baris dengan NaN dihapus.")

    # 5. Map label ke angka
    label_map = {'Negatif': 0, 'Netral': 1, 'Positif': 2}
    df['label_id'] = df['sentimen'].map(label_map)

    # 6. Periksa label yang tidak terpetakan
    if df['label_id'].isnull().sum() > 0:
        print("⚠️ Ada nilai yang tidak dipetakan dengan benar di kolom 'sentimen'.")
        print("Nilai yang tidak dipetakan:", df[df['label_id'].isnull()]['sentimen'].unique())
        df = df.dropna(subset=['label_id'])
        print("✅ Baris dengan label_id NaN dihapus.")
    
    # 7. Pastikan ada data yang tersisa
    if len(df) == 0:
        raise ValueError("Tidak ada data yang valid setelah pemetaan. Periksa nilai yang ada di kolom 'sentimen'.")
    
    # 8. Split data
    X = df['komentar'].tolist()
    y = df['label_id'].values

    # 9. Split Train+Val dan Test
    X_trainval, X_test, y_trainval, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y)
    X_train, X_val, y_train, y_val = train_test_split(
        X_trainval, y_trainval, test_size=0.1, random_state=42, stratify=y_trainval)

    # 10. Tokenisasi
    tokenizer = Tokenizer(num_words=max_words, oov_token="<OOV>")
    tokenizer.fit_on_texts(X_train)

    # 11. Sequences & Padding
    X_train_seq = tokenizer.texts_to_sequences(X_train)
    X_val_seq   = tokenizer.texts_to_sequences(X_val)
    X_test_seq  = tokenizer.texts_to_sequences(X_test)

    X_train_pad = pad_sequences(X_train_seq, maxlen=max_len, padding='post')
    X_val_pad   = pad_sequences(X_val_seq,   maxlen=max_len, padding='post')
    X_test_pad  = pad_sequences(X_test_seq,  maxlen=max_len, padding='post')

    # 12. Save tokenizer + data splits
    with open(tokenizer_path, 'wb') as f:
        pickle.dump(tokenizer, f)
    pd.DataFrame({'komentar': X_train, 'label': y_train}).to_csv("train.csv", index=False)
    pd.DataFrame({'komentar': X_val,   'label': y_val}).to_csv("val.csv",   index=False)
    pd.DataFrame({'komentar': X_test,  'label': y_test}).to_csv("test.csv",  index=False)
    
    # Save padded arrays as numpy
    import numpy as np
    np.save("X_train.npy", X_train_pad)
    np.save("X_val.npy",   X_val_pad)
    np.save("X_test.npy",  X_test_pad)
    np.save("y_train.npy", y_train)
    np.save("y_val.npy",   y_val)
    np.save("y_test.npy",  y_test)

    print("✅ Preprocessing selesai. Tokenizer & data splits sudah disimpan.")

if __name__ == "__main__":
    run()
