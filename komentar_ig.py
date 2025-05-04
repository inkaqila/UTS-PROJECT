import pandas as pd

# Baca file komentar Instagram
df = pd.read_csv("komentar_instagram.csv")  # Ganti sesuai nama file kamu

# Ambil hanya kolom 'Comment' dan ubah nama kolom jadi 'komentar'
df_ig = df[['Comment']].rename(columns={'Comment': 'komentar'})

# Simpan ke file baru (opsional)
df_ig.to_csv("komentar_instagram_only.csv", index=False)

print("✅ Kolom 'Comment' berhasil disimpan sebagai 'komentar' di 'komentar_instagram_only.csv'")
print(df_ig.head())
