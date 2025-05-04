import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# 1. Baca dataset berlabel (ganti nama file sesuai milikmu)
df = pd.read_csv('dataset_label.csv')

# 2. Gabungkan semua komentar menjadi satu string
all_comments = ' '.join(df['komentar'].dropna())

# 3. Buat WordCloud
wordcloud = WordCloud(
    background_color='white', 
    width=800, 
    height=400, 
    max_words=200,
    colormap='viridis'  # Bisa diganti colormap lain seperti 'plasma', 'cool', dll
).generate(all_comments)

# 4. Visualisasikan dan simpan sebagai PNG
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.tight_layout()
plt.savefig('static/wordcloud.png')  # Simpan di folder static
plt.show()
