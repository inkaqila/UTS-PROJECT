import pandas as pd
import re

# Gunakan file hasil scraping yang benar
file_input = "dataset_komentar.csv"
file_output = "dataset_clean.csv"

# Baca file CSV (pastikan ada kolom 'komentar')
df = pd.read_csv(file_input)

# Cek jika kolom 'komentar' ada
if 'komentar' not in df.columns:
    raise ValueError("Kolom 'komentar' tidak ditemukan di dalam dataset.")

# Function untuk membersihkan teks komentar
def bersihkan_komentar(text):
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)  # non-ASCII
    text = re.sub(r'http[s]?\:\/\/\S+', ' ', text)  # URL
    text = re.sub(r'pic.twitter.com\S+', ' ', text)  # pic.twitter
    text = re.sub(r'\@[\w]+', ' ', text)  # mention
    text = re.sub(r'[!$%^&*@#()_+|~=`{}\[\]%\-:";\'<>?,.\/]', ' ', text)  # simbol
    text = re.sub(r'[0-9]+', '', text)  # angka
    text = re.sub(r'([a-zA-Z])\1\1+', r'\1', text)  # duplikasi 3+ huruf
    text = re.sub(r' +', ' ', text)  # spasi ganda
    return text.strip().lower()

# Bersihkan semua komentar dan buang duplikat
cleaned_set = set()
cleaned_data = []

for komentar in df['komentar']:
    cleaned = bersihkan_komentar(str(komentar))
    if cleaned and cleaned not in cleaned_set:
        cleaned_set.add(cleaned)
        cleaned_data.append(cleaned)

# Simpan hasil ke file CSV
df_clean = pd.DataFrame({'komentar': cleaned_data})
df_clean.to_csv(file_output, index=False, encoding='utf-8')

print(f"Jumlah tweet sebelum cleaning: {len(df)}")
print(f"Jumlah tweet sesudah cleaning dan deduplikasi: {len(df_clean)}")
print(df_clean.head())
