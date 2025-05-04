import pandas as pd

# Baca file dataset gabungan
df = pd.read_csv("dataset_komentar.csv")

# Cek jumlah baris (data)
jumlah_data = len(df)

print(f"Jumlah data (komentar) dalam file: {jumlah_data}")
