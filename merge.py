import pandas as pd
import glob
import os

def merge_csv_files(output_filename="data_komentar_twitter.csv"):
    # Cari semua file CSV dengan pola nama tertentu
    file_pattern = "komentar_twitter_selenium*.csv"
    file_list = glob.glob(file_pattern)

    if not file_list:
        print("Tidak ada file yang cocok dengan pola:", file_pattern)
        return

    print(f"Menemukan {len(file_list)} file. Menggabungkan...")

    # Baca semua file CSV dan gabungkan
    dataframes = []
    for file in file_list:
        try:
            df = pd.read_csv(file)
            dataframes.append(df)
            print(f"Berhasil membaca: {file} (baris: {len(df)})")
        except Exception as e:
            print(f"Gagal membaca {file}: {e}")

    combined_df = pd.concat(dataframes, ignore_index=True)

    # Simpan hasil gabungan ke file baru
    combined_df.to_csv(output_filename, index=False)
    print(f"Berhasil menyimpan gabungan ke: {output_filename}")
    print(f"Total baris gabungan: {len(combined_df)}")

if __name__ == "__main__":
    merge_csv_files()