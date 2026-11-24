class Pengguna:
    def __init__(self, username):
        if not username.strip():
            raise ValueError("Username tidak boleh kosong")
        self.__username = username
 
    @property
    def username(self):
        return self.__username
 
    def buat_file(self, jenis, nama, ukuran, **kwargs):
        if jenis == "dokumen":
            return Dokumen(nama, ukuran, self, **kwargs)
        if jenis == "gambar":
            return Gambar(nama, ukuran, self, **kwargs)
        if jenis == "video":
            return Video(nama, ukuran, self, **kwargs)
        raise ValueError("Jenis file tidak dikenal")
 
    def buat_folder(self, nama):
        return Folder(nama, self)
 
    def akses_file(self, file):
        if file.pemilik == self:
            return file.baca()
        if file.hak_akses.boleh_baca():
            return file.baca()
        return "Akses ditolak"
 
 
class HakAkses:
    def __init__(self, read=True, write=False):
        self.__read = read
        self.__write = write
 
    @property
    def read(self):
        return self.__read
 
    @property
    def write(self):
        return self.__write
 
    def boleh_baca(self):
        return self.__read
 
    def boleh_tulis(self):
        return self.__write
 
    def ubah_izin(self, read, write):
        if not isinstance(read, bool) or not isinstance(write, bool):
            raise ValueError("Izin harus berupa boolean")
        self.__read = read
        self.__write = write
 
 
class File:
    jumlah_file = 0  # Class attribute
 
    def __init__(self, nama, ukuran, pemilik):
        if not self.validasi_nama(nama):
            raise ValueError("Nama file tidak valid")
        self.__nama = nama
        self.__ukuran = 0
        self.ukuran = ukuran
        self.__pemilik = pemilik
        self.__hak_akses = HakAkses()  # Composition
        File.jumlah_file += 1
 
    @staticmethod
    def validasi_nama(nama):
        return isinstance(nama, str) and bool(nama.strip())
 
    @property
    def nama(self):
        return self.__nama
 
    @property
    def ukuran(self):
        return self.__ukuran
 
    @ukuran.setter
    def ukuran(self, nilai):
        if not isinstance(nilai, (int, float)):
            raise ValueError("Ukuran harus berupa angka")
        if isinstance(nilai, bool) or nilai < 0:
            raise ValueError("Ukuran tidak boleh negatif")
        self.__ukuran = nilai
 
    @property
    def pemilik(self):
        return self.__pemilik
 
    @property
    def hak_akses(self):
        return self.__hak_akses
 
    def baca(self):
        if not self.__hak_akses.boleh_baca():
            return "File tidak dapat dibaca"
        return f"Membaca file: {self.__nama}"
 
    def tulis(self, isi):
        if not self.__hak_akses.boleh_tulis():
            return "Izin menulis ditolak"
        return f"Isi file {self.__nama} diperbarui"
 
    def info(self):
        return f"{self.__nama} ({self.__ukuran} MB)"
 
    def __str__(self):
        return f"{self.__nama} - {self.__ukuran} MB"
 
    def __eq__(self, lain):
        if not isinstance(lain, File):
            return NotImplemented
        return self.nama == lain.nama and self.pemilik == lain.pemilik
 
 
class Dokumen(File):
    def __init__(self, nama, ukuran, pemilik, format="PDF"):
        super().__init__(nama, ukuran, pemilik)
        self.__format = format
 
    def baca(self):
        return f"Membuka dokumen {self.nama} ({self.__format})"
 
 
class Gambar(File):
    def __init__(self, nama, ukuran, pemilik, resolusi="1920x1080"):
        super().__init__(nama, ukuran, pemilik)
        self.__resolusi = resolusi
 
    def info(self):
        return f"{self.nama} - resolusi {self.__resolusi}"
 
 
class Video(File):
    def __init__(self, nama, ukuran, pemilik, durasi=0):
        super().__init__(nama, ukuran, pemilik)
        self.__durasi = durasi
 
    def info(self):
        return f"{self.nama} - durasi {self.__durasi} detik"
 
 
class Folder:
    def __init__(self, nama, pemilik):
        if not nama.strip():
            raise ValueError("Nama folder tidak boleh kosong")
        self.__nama = nama
        self.__pemilik = pemilik
        self.__isi = []
 
    @property
    def nama(self):
        return self.__nama
 
    @property
    def pemilik(self):
        return self.__pemilik
 
    def tambah_item(self, item):
        if not isinstance(item, (File, Folder)):
            raise TypeError("Isi folder harus berupa File atau Folder")
        if item not in self.__isi:
            self.__isi.append(item)
 
    def buat_subfolder(self, nama):
        subfolder = Folder(nama, self.__pemilik)  # Composition
        self.tambah_item(subfolder)
        return subfolder
 
    def hapus_item(self, item):
        if item in self.__isi:
            self.__isi.remove(item)
            return True
        return False
 
    def tampilkan_isi(self):
        if not self.__isi:
            return f"Folder {self.__nama} kosong"
        daftar = ", ".join(item.nama for item in self.__isi)
        return f"Isi folder {self.__nama}: {daftar}"
    


if __name__ == "__main__":
    pemilik = Pengguna("purata")
    folder = pemilik.buat_folder("Tugas Kuliah")
 
    dokumen = pemilik.buat_file(
        "dokumen", "Laporan", 2.5, format="PDF"
    )
    gambar = pemilik.buat_file(
        "gambar", "Diagram", 1.2, resolusi="1920x1080"
    )
    video = pemilik.buat_file(
        "video", "Presentasi", 50, durasi=300
    )
 
    # Aggregation: file yang telah dibuat dimasukkan ke folder
    folder.tambah_item(dokumen)
    folder.tambah_item(gambar)
    folder.tambah_item(video)
 
    print(folder.tampilkan_isi())
    print(dokumen.baca())
    print(gambar.info())
    print(video.info())
 
    try:
        dokumen.ukuran = -5
    except ValueError as error:
        print("Validasi:", error)
 
    dokumen_duplikat = pemilik.buat_file(
        "dokumen", "Laporan", 2.5, format="PDF"
    )
    print("Dokumen sama:", dokumen == dokumen_duplikat)
    print("Jumlah file:", File.jumlah_file)
    print("Detail:", dokumen)
    print("Akses pemilik:", pemilik.akses_file(dokumen))

