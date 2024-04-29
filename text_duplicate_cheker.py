import pandas as pd
import os


def cek_duplikat_case_insensitive(old_titles, new_titles):
    duplikat = set()
    set1 = set(map(str.lower, old_titles))
    set2 = set(map(str.lower, new_titles))

    for kalimat in set1.intersection(set2):
        duplikat.add(kalimat)

    return list(duplikat)


current_dir = os.path.abspath(os.getcwd())

# Membaca data dari file Excel
current_dir = os.path.abspath(os.getcwd())

# Ganti dengan path file Excel pertama
old_titles_path = fr"{current_dir}\data_excel\old_titles.xlsx"
# Ganti dengan path file Excel kedua
new_titles_path = fr"{current_dir}\data_excel\titles.xlsx"

# Menggunakan pandas untuk membaca data dari file Excel
df1 = pd.read_excel(old_titles_path)
df2 = pd.read_excel(new_titles_path)

# Mengambil kolom dengan kumpulan kalimat
# Ganti 'Nama Kolom Kalimat' dengan nama kolom sesuai file Excel
old_titles = df1['judul'].tolist()
# Ganti 'Nama Kolom Kalimat' dengan nama kolom sesuai file Excel
new_titles = df2['judul'].tolist()

# Contoh penggunaan
diplicate_titles = cek_duplikat_case_insensitive(old_titles, new_titles)

if diplicate_titles:
    print("Kalimat duplikat yang terdeteksi:")
    for duplicate_title in diplicate_titles:
        print(f'"{duplicate_title}"')
else:
    print("Tidak ada kalimat duplikat.")
