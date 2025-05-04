import numpy as np
from keras.models import Sequential, load_model
from keras.layers import Embedding, LSTM, Dropout, Dense


def train_and_save(max_words=10000, max_len=100, model_path="lstm_model.h5"):
    # 1. Load data
    X_train = np.load("X_train.npy")
    X_val   = np.load("X_val.npy")
    y_train = np.load("y_train.npy")
    y_val   = np.load("y_val.npy")

    # 2. Hitung vocab size dari tokenizer.pkl
    import pickle
    with open('tokenizer.pkl', 'rb') as f:
        tokenizer = pickle.load(f)
    vocab_size = min(max_words, len(tokenizer.word_index) + 1)

    # 3. Definisikan model LSTM
    model = Sequential([
        Embedding(input_dim=vocab_size, output_dim=128, input_length=max_len),
        LSTM(64),
        Dropout(0.5),
        Dense(3, activation='softmax')
    ])
    model.compile(
        loss='sparse_categorical_crossentropy',
        optimizer='adam',
        metrics=['accuracy']
    )

    # 4. Latih model
    history = model.fit(
        X_train, y_train,
        epochs=5,
        batch_size=32,
        validation_data=(X_val, y_val)
    )

    # 5. Simpan model
    model.save(model_path)
    print(f"✅ Model LSTM tersimpan sebagai: {model_path}")

if __name__ == "__main__":
    train_and_save()
