import pandas as pd
import csv 

def gabung_dan_perbaiki_csv(file_twitter, file_instagram, output_file):
    # Baca hanya kolom 'komentar' dari masing-masing file
    df_twitter = pd.read_csv(file_twitter, usecols=["komentar"])
    df_instagram = pd.read_csv(file_instagram, usecols=["komentar"])

    # Gabungkan keduanya
    df_gabungan = pd.concat([df_twitter, df_instagram], ignore_index=True)

    # Simpan ulang dengan benar, pakai quoting agar koma tidak bikin kolom baru
    df_gabungan.to_csv(output_file, index=False, encoding="utf-8", quoting=csv.QUOTE_ALL)

    print(f"File gabungan berhasil disimpan sebagai: {output_file}")
    print(f"Total komentar: {len(df_gabungan)}")

if __name__ == "__main__":
    gabung_dan_perbaiki_csv(
        file_twitter="komentar_twitter_only.csv",
        file_instagram="komentar_instagram_only.csv",
        output_file="dataset_komentar.csv"
    )
