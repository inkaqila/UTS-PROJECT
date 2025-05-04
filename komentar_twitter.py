import pandas as pd

# Baca file CSV asli
df = pd.read_csv("data_komentar_twitter.csv")  # Ganti nama file jika beda

# Ambil hanya kolom 'komentar'
df_komentar = df[['komentar']]

# Simpan ke file baru (opsional)
df_komentar.to_csv("komentar_twitter_only.csv", index=False)

print("✅ Kolom 'komentar' berhasil disimpan ke 'komentar_twitter_only.csv'")
print(df_komentar.head())
