import random
import shutil
import os
import pandas as pd
import time
import auto_uploader

current_dir = os.path.abspath(os.getcwd())


def ceheck_duplicate_case_insensitive_titles(old_titles, new_titles):
    duplikat = set()
    set1 = set(map(str.lower, old_titles))
    set2 = set(map(str.lower, new_titles))

    for kalimat in set1.intersection(set2):
        duplikat.add(kalimat)

    return list(duplikat)


def move_new_titles_to_old_titles(new_titles, old_titles):
    # Baca file Excel sumber yang berisi daftar judul
    df_sumber = pd.read_excel(new_titles)

    # Baca file Excel tujuan
    try:
        df_tujuan = pd.read_excel(old_titles)
    except FileNotFoundError:
        # Jika file tujuan belum ada, buat dataframe kosong
        df_tujuan = pd.DataFrame(columns=['judul'])

    # Gabungkan data dari file sumber ke file tujuan tanpa menghilangkan data lama
    df_tujuan = pd.merge(df_tujuan, df_sumber, how='outer')

    # Hapus duplikat berdasarkan kolom "judul"
    df_tujuan.drop_duplicates(subset=['judul'], keep='first', inplace=True)

    # Tulis dataframe hasil ke file Excel tujuan
    df_tujuan.to_excel(old_titles, index=False)

    # Hapus isinya saja (tanpa menghapus file)
    df_sumber.iloc[0:0].to_excel(new_titles, index=False)

    print(f"Entri baru berhasil ditambahkan ke {old_titles}.")
    print(f"Isi dari {new_titles} telah dihapus.")


def create_folders(num_folders, base_folder_name_to_create):
    base_folder = fr"{current_dir}\products"
    count = 0
    for i in range(1, num_folders + 1):
        folder_name = f"{base_folder}/{base_folder_name_to_create}_{i}"
        images_folder = f"{folder_name}/images"

        # Membuat folder utama
        os.makedirs(folder_name, exist_ok=True)

        # Membuat subfolder "images"
        os.makedirs(images_folder, exist_ok=True)
        count += 1
    print(f"{count} Folder dengan nama dasar '{base_folder_name_to_create}' dan subfolder 'images' berhasil dibuat.")


def move_images_to_folders(num_folders, base_product_folder_name, num_images_per_folder, base_images_folder_name):
    base_images_path = fr"{current_dir}\base_images\{base_images_folder_name}"
    base_products_path = fr"{current_dir}\products"

    for i in range(1, num_folders + 1):
        folder_name = f"{base_product_folder_name}_{i}"
        images_folder = os.path.join(
            base_products_path, folder_name, "images")

        # Membuat folder "images" jika belum ada
        os.makedirs(images_folder, exist_ok=True)

        # Mengambil 5 gambar secara acak dari "base_images"
        images_to_move = random.sample(os.listdir(
            base_images_path), num_images_per_folder)

        # Memindahkan gambar ke folder "images" pada masing-masing folder
        for image in images_to_move:
            image_path_src = os.path.join(base_images_path, image)
            image_path_dest = os.path.join(images_folder, image)
            shutil.move(image_path_src, image_path_dest)
    print(f"{num_folders} gambar berhasil dipindahkan ke {images_folder}")


def create_txt_files(products_folder, new_titles_path):
    try:
        # Membaca file Excel
        new_titles_df = pd.read_excel(new_titles_path)
        product_subfolders = os.listdir(products_folder)

        # Memastikan jumlah judul sama dengan jumlah subfolder
        if len(new_titles_df) < len(product_subfolders):
            print(
                f"Terjadi kesalahan: Jumlah judul pada file excel {len(new_titles_df)} tidak sama dengan jumlah subfolder {len(product_subfolders)}.")
            return False

        # Iterasi melalui setiap subfolder
        for i, subfolder in enumerate(product_subfolders):
            subfolder_path = os.path.join(products_folder, subfolder)
            title_txt_file_path = os.path.join(subfolder_path, "info.txt")

            # Membuat file teks dengan judul produk dari file Excel
            with open(title_txt_file_path, "w") as title_txt:
                title = new_titles_df.at[i, "judul"]
                title_txt.write(f"judul : {title}\n")

            print(f"File 'info.txt' di dalam {subfolder} berhasil dibuat.")

        print("Pembuatan file txt selesai.")
        return True
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")
        return False


def move_images_to_base_images():
    base_images_folder_name = input("Masukkan nama folder gambar: ")
    products_folder = fr"{current_dir}\products"
    base_images_path = fr"{current_dir}\base_images\{base_images_folder_name}"

    try:
        # Mengakses setiap subfolder di dalam folder "products"
        for subfolder in os.listdir(products_folder):
            subfolder_path = os.path.join(products_folder, subfolder)
            images_folder = os.path.join(subfolder_path, "images")

            # Memastikan folder "images" ada di dalam subfolder
            if os.path.exists(images_folder):
                # Mengakses setiap gambar di dalam folder "images" dan memindahkannya ke "base_images"
                for image in os.listdir(images_folder):
                    image_path_src = os.path.join(images_folder, image)
                    image_path_dest = os.path.join(base_images_path, image)

                    # Memindahkan gambar
                    shutil.move(image_path_src, image_path_dest)
                    print(
                        f"Gambar {image} dipindahkan ke {base_images_path}")

                # Menghapus folder "images" setelah semua gambarnya dipindahkan
                shutil.rmtree(images_folder)
                print(
                    f"Folder 'images' di dalam {subfolder} dihapus setelah pemindahan gambar.")

        print("Pemindahan gambar selesai.")
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")


def delete_products_subfolders():
    products_folder = fr"{current_dir}\products"
    try:
        # Menghapus seluruh isi folder "products"
        shutil.rmtree(products_folder)
        print(f"Isi folder {products_folder} berhasil dihapus.")
    except FileNotFoundError:
        print(f"Folder {products_folder} tidak ditemukan.")
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")


def start_menus():
    print("""Pilih menu yang ingin dijalankan:
    1. Buat folder dan subfolder
    2. Pindahkan gambar ke folder products
    3. Buat judul untuk setiap subfolder products
    4. Hapus semua folder di dalam folder products
    5. Pindahkan semua gambar dari sub folder products kembali ke base_images
    6. Cek duplicate judul
    7. Buat folder, subfolder, pindahkan gambar dan buat txt
    8. Pindahkan judul baru ke judul lama
    9. Upload produk
    10. Keluar
        """)
    option = input("Masukkan pilihan [1/2/3..]: ")
    return option


def start():
    while True:
        new_titles_path = fr"{current_dir}\data_excel\titles.xlsx"
        old_titles_path = fr"{current_dir}\data_excel\old_titles.xlsx"
        products_folder_path = fr"{current_dir}\products"
        error_message = "Pilihan yang anda masukkan tidak sesuai. Masukkan angka saja"
        if not os.path.exists(products_folder_path):
            os.makedirs(products_folder_path, exist_ok=True)
        if os.path.exists(products_folder_path):
            product_subfolders = os.listdir(products_folder_path)
            try:
                new_titles_df = pd.read_excel(new_titles_path)
            except FileNotFoundError:
                print(
                    "\nFile Excel judul tidak ditemukan. Silahkan buat terlebih dahulu.")
                break
            if len(new_titles_df) == 0:
                print(
                    "\nJudul pada file excel kosong. Silahkan perbaiki file excel judul terlebih dahulu.")
                break
            if len(new_titles_df) < len(product_subfolders):
                print("\nJumlah judul pada file excel tidak sesuai dengan jumlah produk. Silahkan perbaiki file excel judul terlebih dahulu.")
                break
        option = start_menus()
        try:
            option = int(option)
        except:
            print(error_message)
            continue
        if isinstance(option, int) and option <= 10 and option >= 1:
            # buat subfolder di folder products
            if option == 1:
                # Masukkan jumlah folder yang ingin dibuat
                number_folders = int(
                    input("Masukkan jumlah folder yang ingin dibuat: "))
                base_folder_name = input(
                    "Masukkan nama utama folder yang ingin dibuat: ")

                # Panggil fungsi untuk membuat folder dan subfolder
                create_folders(number_folders, base_folder_name)
                continue

            # pindahkan gambar dari base images ke folder images
            if option == 2:
                if len(product_subfolders) == 0:
                    print("Sub folder pada folder produk kosong. Buat terlebih dahulu.")
                    continue
                number_images = int(
                    input("Masukkan jumlah gambar yang ingin dipindahkan di tiap folder images: "))
                base_product_folder_name = input(
                    "Masukkan nama utama folder tujuan: ")
                base_images_folder_name = input(
                    "Masukkan nama folder gambar: ")
                if (len(product_subfolders)*number_images) > base_images_count:
                    print(
                        f"Jumlah gambar tidak mencukupi untuk membuat {number_folders} folder. Silahkan tambahkan gambar terlebih dahulu")
                    continue
                move_images_to_folders(
                    len(product_subfolders), base_product_folder_name, number_images, base_images_folder_name)
                continue

            # Panggil fungsi untuk membuat file txt di setiap subfolder
            if option == 3:
                create_txt_files(products_folder_path, new_titles_path)
                continue

            # hapus semua folder di dalam folder products
            if option == 4:
                is_delete = input(
                    "Apakah anda ingin menghapus semua folder di dalam folder products? (y/n): ").lower()
                if is_delete == "y":
                    delete_products_subfolders()
                continue

            # pindahkan semua gambar kembali ke base images
            if option == 5:
                is_move_image_back = input(
                    "Apakah anda ingin memindahkan semua gambar dari sub folder products kembali ke base_images? (y/n): ").lower()
                if is_move_image_back == "y":
                    move_images_to_base_images()
                continue

            # cek diplicate titles
            if option == 6:
                # Menggunakan pandas untuk membaca data dari file Excel
                df1 = pd.read_excel(old_titles_path)
                df2 = pd.read_excel(new_titles_path)

                # Mengambil kolom dengan kumpulan kalimat
                # Ganti 'Nama Kolom Kalimat' dengan nama kolom sesuai file Excel
                old_titles = df1['judul'].tolist()
                # Ganti 'Nama Kolom Kalimat' dengan nama kolom sesuai file Excel
                new_titles = df2['judul'].tolist()

                # Contoh penggunaan
                diplicate_titles = ceheck_duplicate_case_insensitive_titles(
                    old_titles, new_titles)

                if diplicate_titles:
                    print("Kalimat duplikat yang terdeteksi:")
                    for duplicate_title in diplicate_titles:
                        print(f'"{duplicate_title}"')
                    continue
                else:
                    print("Tidak ada judul duplikat.\n")
                    time.sleep(1)
                    continue

            # buat products, images, txt
            if option == 7:
                number_folders = int(
                    input("Masukkan jumlah folder yang ingin dibuat: "))
                base_folder_name = input(
                    "Masukkan nama utama folder yang ingin dibuat: ")
                number_images = int(
                    input("Masukkan jumlah gambar yang ingin dipindahkan di tiap folder images: "))
                base_images_folder_name = input(
                    "Masukkan nama folder gambar: ")
                base_images_count = len(os.listdir(
                    fr"{current_dir}\base_images\{base_images_folder_name}"))
                if (number_folders*number_images) > base_images_count:
                    print(
                        f"Jumlah gambar tidak mencukupi untuk membuat {number_folders} folder. Silahkan tambahkan gambar terlebih dahulu")
                    continue
                create_folders(number_folders, base_folder_name)
                move_images_to_folders(
                    number_folders, base_folder_name, number_images, base_images_folder_name)

                # Panggil fungsi untuk membuat file txt di setiap subfolder
                create_txt_files(products_folder_path, new_titles_path)
                continue

            # pindah judul baru ke judul lama
            if option == 8:
                move_new_titles_to_old_titles(new_titles_path, old_titles_path)
                continue
            if option == 9:
                is_upload = input(
                    "Pastikan folder produk sesuai terlebih dahulu. Apakah anda ingin mengupload produk? (y/n): ").lower()
                if len(product_subfolders) == 0:
                    print("\nWARNING!!!")
                    print(
                        "Sub folder pada folder produk kosong. Tambahkan terlebih dahulu\n")
                    continue
                if is_upload == "y":
                    auto_uploader.main()
                continue
            if option == 10:
                break
        else:
            print(error_message)
            continue


start()
