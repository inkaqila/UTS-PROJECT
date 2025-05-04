import pandas as pd
import matplotlib.pyplot as plt

# 1. Baca dataset berlabel
df = pd.read_csv('dataset_label.csv')

# 2. Hitung jumlah tiap kelas
sentiment_counts = df['sentimen'].value_counts().sort_index()

# 3. Siapkan warna
colors = {
    'negative': '#FF6F61',
    'neutral':  '#6B5B95',
    'positive': '#88B04B'
}
bar_colors = [colors[label] for label in sentiment_counts.index]

# 4. Buat bar chart
plt.figure(figsize=(8, 5))
bars = plt.bar(sentiment_counts.index, sentiment_counts.values, color=bar_colors)
plt.title('Sebaran Kelas Sentimen')
plt.xlabel('Kelas Sentimen')
plt.ylabel('Jumlah Komentar')

# 5. Tambah label angka di atas batang
for bar in bars:
    h = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, h + 2, f'{int(h)}', ha='center', va='bottom', fontweight='bold')

plt.tight_layout()
plt.savefig("static/sentiment_distribution.png")  # ✅ Simpan gambar
plt.show()
