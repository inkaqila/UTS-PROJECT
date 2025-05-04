# from flask import Flask, render_template, request
# import numpy as np
# import pickle
# from keras.models import load_model
# from keras.preprocessing.sequence import pad_sequences
# import matplotlib.pyplot as plt
# from wordcloud import WordCloud
# import os

# app = Flask(__name__)

# # Load tokenizer dan model
# with open('tokenizer.pkl', 'rb') as f:
#     tokenizer = pickle.load(f)

# model = load_model('lstm_model.h5')
# labels = {0: "Negatif", 1: "Netral", 2: "Positif"}

# def predict_sentiment(text):
#     sequence = tokenizer.texts_to_sequences([text])
#     padded = pad_sequences(sequence, maxlen=100)
#     prediction = model.predict(padded)[0]
#     label = np.argmax(prediction)
#     return labels[label], prediction

# @app.route("/", methods=["GET", "POST"])
# def index():
#     result = None
#     confidence = None
#     text = ""
#     if request.method == "POST":
#         text = request.form["komentar"]
#         result, confs = predict_sentiment(text)
#         confidence = round(float(np.max(confs)) * 100, 2)
#     return render_template("index.html", result=result, confidence=confidence, text=text)

# @app.route("/visualisasi")
# def visualisasi():
#     return render_template("visualisasi.html")

# if __name__ == "__main__":
#     app.run(debug=True)

# app.py
from flask import Flask, render_template, request
import numpy as np
import pickle
from tensorflow.keras.models import load_model

app = Flask(__name__)

# Load model & tokenizer
model = load_model("lstm_model.h5")
with open("tokenizer.pkl", "rb") as f:
    tokenizer = pickle.load(f)

max_len = 100

def preprocess_input(text):
    from tensorflow.keras.preprocessing.sequence import pad_sequences
    sequences = tokenizer.texts_to_sequences([text])
    padded = pad_sequences(sequences, maxlen=max_len)
    return padded

@app.route("/", methods=["GET", "POST"])
def index():
    prediction = None
    if request.method == "POST":
        komentar = request.form["komentar"]
        input_seq = preprocess_input(komentar)
        pred = model.predict(input_seq)
        label = np.argmax(pred)

        labels_map = {0: "Negatif", 1: "Netral", 2: "Positif"}
        prediction = labels_map[label]

    return render_template("index.html", prediction=prediction)

@app.route("/statistic")
def statistic():
    return render_template("statistic.html")

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
  


