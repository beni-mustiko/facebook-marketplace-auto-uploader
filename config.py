import os

current_dir = os.path.abspath(os.getcwd())

fb_email = "your@email"
fb_password = "your_password"

# harga berupa rentang harga ex: 12000 sampai 14000 kelipatan 1000
price = [28000, 28001, 1]

color = "Putih"
# locations = ["bantul"]
locations = ["sleman", "yogyakarta"]

# description = """
# Bantal Natal Custom merupakan pilihan sempurna untuk menambahkan sentuhan khusus pada perayaan Natal Anda. Anda dapat memesan bantal sesuai keinginan, mulai dari ukuran, desain, dan warna, bantal-bantal ini memungkinkan Anda menciptakan kenangan yang unik sesuai dengan selera dan gaya pribadi Anda. Dengan berbagai motif Natal yang unik, setiap bantal memberikan nuansa hangat dan keceriaan dalam suasana liburan. Kualitas premium dari bahan Dakron atau Dacron memastikan kenyamanan dan daya tahan, sementara harga yang terjangkau membuatnya menjadi pilihan souvenir Natal yang istimewa. Dapatkan kenangan hangat dan indah dengan Bantal Natal Custom ini, yang juga tersedia dari Bantalindo untuk memastikan kualitas dan kreativitas yang tak tertandingi.

# Ready, langsung WA 085156911828"""

# description = """
# Disini pusatnya Busa lembaran harga kiloan,.jelas lebih hemat 100%
# Kriteria busa : keras - ringan
# Produk terbatas, siapa cepat dapat dan pastinya Free ongkir

# Kirim bayar ditempat juga bisa, ambil di gudang juga bisa
# Harga Santai bisa dibicarakan Untuk pengambilan rutin, tanya-tanya dulu boleh
# Ecer atau grosir bisa COD semua harga bisa di bicarakan

# Ready, langsung WA 085156911828"""

description = """
Disini pusatnya Bantal Tidur Kualitas Hotel. Jelas lebih hemat 100%
Produk terbatas, siapa cepat dapat.
Promo akhir tahun, harga 28000 tanpa minimal pembelian

Kirim bayar ditempat juga bisa, ambil di gudang juga bisa
Harga Santai bisa dibicarakan Untuk pengambilan rutin, tanya-tanya dulu boleh
Ecer atau grosir bisa COD semua harga bisa di bicarakan

Ready, langsung WA 0851 7971 4541"""

labels = ["bantal", "bantal tidur", "bantal hotel", "bantal kepala",
          "bantal dakron", "bantal silikon", "bantal dacron", "guling", "guling hotel"]
# labels = ["kasur busa", "inoac", "royal foam", "busa", "kasur lipat", "toko busa",
#           "toko kasur busa"]

# labels = ["bantal", "souvenir", "natal", "bantal natal", "bantal natal custom", "bantal custom",
#           "banatl souvenir" "bantal sofa", "bantal dakron", "dakron", "dacron", "slikon", "silicon", "bantal cinta"]
# labels = [
#     "busa", "springbed", "kasur", "royal foam", "kiloan", "limbah", "inoac", "kasur busa", "sofa", "spring bed", "busa kiloan", "busa limbah", "busa lembaran", "harga murah", "cod", "matras", "bahan sofa", "bahan jok", "busa daging", "serenity"]

json_file_path_and_filename = os.path.join(
    fr"{current_dir}\data_json", "product_informations.json")

chrome_driver_path = fr"{current_dir}\chrome_driver\chromedriver.exe"
products_folder = fr"{current_dir}\products"

products_informations_json_path = fr"{current_dir}\data_json"
json_filename = "product_informations.json"
