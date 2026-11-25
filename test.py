# ============================================================
# SISTEM MANAJEMEN FILE
# Gabungan dari:
# exceptions.py, hak_akses.py, file.py, folder.py,
# pengguna.py, dan main.py
# ============================================================


# ============================================================
# 1. CUSTOM EXCEPTIONS
# ============================================================

class SistemFileError(Exception):
    """Exception dasar untuk sistem manajemen file."""
    pass


class ValidasiDataError(SistemFileError, ValueError):
    """Terjadi ketika data tidak memenuhi aturan validasi."""
    pass


class AksesDitolakError(SistemFileError, PermissionError):
    """Terjadi ketika pengguna tidak memiliki izin."""
    pass


class JenisFileError(SistemFileError, ValueError):
    """Terjadi ketika jenis file tidak dikenal."""
    pass


class StrukturFolderError(SistemFileError, TypeError):
    """Terjadi ketika isi folder tidak valid."""
    pass


# ============================================================
# 2. CLASS HAK AKSES
# ============================================================

class HakAkses:
    def __init__(self, read=True, write=False):
        if not isinstance(read, bool) or not isinstance(write, bool):
            raise ValidasiDataError("Izin harus berupa boolean")

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
            raise ValidasiDataError("Izin harus berupa boolean")

        self.__read = read
        self.__write = write
        return "Hak akses berhasil diperbarui"


# ============================================================
# 3. CLASS FILE DAN TURUNANNYA
# ============================================================

class File:
    jumlah_file = 0

    def __init__(self, nama, ukuran, pemilik):
        if not self.validasi_nama(nama):
            raise ValidasiDataError("Nama file tidak valid")

        self.__nama = nama
        self.__ukuran = 0
        self.ukuran = ukuran
        self.__pemilik = pemilik
        self.__hak_akses = HakAkses()
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
        if not isinstance(nilai, (int, float)) or isinstance(nilai, bool):
            raise ValidasiDataError("Ukuran harus berupa angka")

        if nilai < 0:
            raise ValidasiDataError("Ukuran tidak boleh negatif")

        self.__ukuran = nilai

    @property
    def pemilik(self):
        return self.__pemilik

    @property
    def hak_akses(self):
        return self.__hak_akses

    def baca(self):
        if not self.__hak_akses.boleh_baca():
            raise AksesDitolakError("File tidak dapat dibaca")

        return f"Membaca file: {self.__nama}"

    def tulis(self, isi):
        if not self.__hak_akses.boleh_tulis():
            raise AksesDitolakError("Izin menulis ditolak")

        return f"Isi file {self.__nama} diperbarui"

    def info(self):
        return f"{self.__nama} ({self.__ukuran} MB)"

    def __str__(self):
        return f"{self.__nama} - {self.__ukuran} MB"

    def __eq__(self, lain):
        if not isinstance(lain, File):
            return NotImplemented

        return (
            self.nama == lain.nama
            and self.pemilik == lain.pemilik
        )


class Dokumen(File):
    def __init__(self, nama, ukuran, pemilik, format="PDF"):
        super().__init__(nama, ukuran, pemilik)
        self.__format = format

    def baca(self):
        super().baca()
        return f"Membuka dokumen {self.nama} ({self.__format})"


class Gambar(File):
    def __init__(self, nama, ukuran, pemilik, resolusi="1920x1080"):
        super().__init__(nama, ukuran, pemilik)
        self.__resolusi = resolusi

    def info(self):
        return f"{self.nama} - resolusi {self.__resolusi}"


class Video(File):
    def __init__(self, nama, ukuran, pemilik, durasi=0):
        if (
            not isinstance(durasi, (int, float))
            or isinstance(durasi, bool)
            or durasi < 0
        ):
            raise ValidasiDataError(
                "Durasi video harus berupa angka positif"
            )

        super().__init__(nama, ukuran, pemilik)
        self.__durasi = durasi

    def info(self):
        return f"{self.nama} - durasi {self.__durasi} detik"


# ============================================================
# 4. CLASS FOLDER
# ============================================================

class Folder:
    def __init__(self, nama, pemilik):
        if not isinstance(nama, str) or not nama.strip():
            raise ValidasiDataError("Nama folder tidak boleh kosong")

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
            raise StrukturFolderError(
                "Isi folder harus berupa File atau Folder"
            )

        if item not in self.__isi:
            self.__isi.append(item)

    def buat_subfolder(self, nama):
        subfolder = Folder(nama, self.__pemilik)
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


# ============================================================
# 5. CLASS PENGGUNA
# ============================================================

class Pengguna:
    def __init__(self, username):
        if not isinstance(username, str) or not username.strip():
            raise ValidasiDataError("Username tidak boleh kosong")

        self.__username = username

    @property
    def username(self):
        return self.__username

    def buat_file(self, jenis, nama, ukuran, **kwargs):
        if jenis == "dokumen":
            return Dokumen(nama, ukuran, self, **kwargs)

        elif jenis == "gambar":
            return Gambar(nama, ukuran, self, **kwargs)

        elif jenis == "video":
            return Video(nama, ukuran, self, **kwargs)

        else:
            raise JenisFileError("Jenis file tidak dikenal")

    def buat_folder(self, nama):
        return Folder(nama, self)

    def akses_file(self, file):
        if not isinstance(file, File):
            raise ValidasiDataError("Objek yang diakses bukan file")

        if file.pemilik != self and not file.hak_akses.boleh_baca():
            raise AksesDitolakError("Akses ditolak")

        return file.baca()


# ============================================================
# 6. PROGRAM UTAMA
# ============================================================

def main():
    print("=== SISTEM MANAJEMEN FILE ===")

    try:
        # Membuat pengguna
        pemilik = Pengguna("purata")
        pengguna_lain = Pengguna("anon")

        print("\nPengguna berhasil dibuat")

        # Membuat folder
        folder = pemilik.buat_folder("Tugas Kuliah")

        # Membuat berbagai jenis file
        dokumen = pemilik.buat_file(
            "dokumen", "Laporan", 2.5, format="PDF"
        )

        gambar = pemilik.buat_file(
            "gambar", "Diagram", 1.2,
            resolusi="1920x1080"
        )

        video = pemilik.buat_file(
            "video", "Presentasi", 50, durasi=300
        )

        # Memasukkan file ke folder
        folder.tambah_item(dokumen)
        folder.tambah_item(gambar)
        folder.tambah_item(video)

        print("\n--- Isi Folder ---")
        print(folder.tampilkan_isi())

        # Membaca informasi file
        print("\n--- Informasi File ---")
        print(dokumen.baca())
        print(gambar.info())
        print(video.info())

        # Menguji validasi ukuran
        print("\n--- Pengujian Validasi ---")
        try:
            dokumen.ukuran = -5
        except ValidasiDataError as error:
            print("Validasi berhasil:", error)

        # Menguji jenis file tidak dikenal
        try:
            pemilik.buat_file("musik", "Lagu", 5)
        except SistemFileError as error:
            print("Jenis file:", error)

        # Menguji hak akses
        print("\n--- Pengujian Hak Akses ---")
        dokumen.hak_akses.ubah_izin(
            read=False,
            write=False
        )

        try:
            print(pengguna_lain.akses_file(dokumen))
        except AksesDitolakError as error:
            print("Akses ditolak:", error)

        # Menguji kesamaan file
        dokumen_duplikat = pemilik.buat_file(
            "dokumen", "Laporan", 2.5, format="PDF"
        )

        print("\n--- Informasi Tambahan ---")
        print("Dokumen sama:", dokumen == dokumen_duplikat)
        print("Jumlah file:", File.jumlah_file)
        print("Detail dokumen:", dokumen)

        # Membuat subfolder
        folder.buat_subfolder("Dokumen Tambahan")
        print(folder.tampilkan_isi())

    except SistemFileError as error:
        print("Terjadi kesalahan sistem:", error)

    except Exception as error:
        print("Terjadi kesalahan lain:", error)

    else:
        print("\nProgram berhasil dijalankan.")

    finally:
        print("\nProgram selesai.")


if __name__ == "__main__":
    main()
# ============================================================
# SISTEM MANAJEMEN FILE
# Gabungan dari:
# exceptions.py, hak_akses.py, file.py, folder.py,
# pengguna.py, dan main.py
# ============================================================


# ============================================================
# 1. CUSTOM EXCEPTIONS
# ============================================================

class SistemFileError(Exception):
    """Exception dasar untuk sistem manajemen file."""
    pass


class ValidasiDataError(SistemFileError, ValueError):
    """Terjadi ketika data tidak memenuhi aturan validasi."""
    pass


class AksesDitolakError(SistemFileError, PermissionError):
    """Terjadi ketika pengguna tidak memiliki izin."""
    pass


class JenisFileError(SistemFileError, ValueError):
    """Terjadi ketika jenis file tidak dikenal."""
    pass


class StrukturFolderError(SistemFileError, TypeError):
    """Terjadi ketika isi folder tidak valid."""
    pass


# ============================================================
# 2. CLASS HAK AKSES
# ============================================================

class HakAkses:
    def __init__(self, read=True, write=False):
        if not isinstance(read, bool) or not isinstance(write, bool):
            raise ValidasiDataError("Izin harus berupa boolean")

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
            raise ValidasiDataError("Izin harus berupa boolean")

        self.__read = read
        self.__write = write
        return "Hak akses berhasil diperbarui"


# ============================================================
# 3. CLASS FILE DAN TURUNANNYA
# ============================================================

class File:
    jumlah_file = 0

    def __init__(self, nama, ukuran, pemilik):
        if not self.validasi_nama(nama):
            raise ValidasiDataError("Nama file tidak valid")

        self.__nama = nama
        self.__ukuran = 0
        self.ukuran = ukuran
        self.__pemilik = pemilik
        self.__hak_akses = HakAkses()
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
        if not isinstance(nilai, (int, float)) or isinstance(nilai, bool):
            raise ValidasiDataError("Ukuran harus berupa angka")

        if nilai < 0:
            raise ValidasiDataError("Ukuran tidak boleh negatif")

        self.__ukuran = nilai

    @property
    def pemilik(self):
        return self.__pemilik

    @property
    def hak_akses(self):
        return self.__hak_akses

    def baca(self):
        if not self.__hak_akses.boleh_baca():
            raise AksesDitolakError("File tidak dapat dibaca")

        return f"Membaca file: {self.__nama}"

    def tulis(self, isi):
        if not self.__hak_akses.boleh_tulis():
            raise AksesDitolakError("Izin menulis ditolak")

        return f"Isi file {self.__nama} diperbarui"

    def info(self):
        return f"{self.__nama} ({self.__ukuran} MB)"

    def __str__(self):
        return f"{self.__nama} - {self.__ukuran} MB"

    def __eq__(self, lain):
        if not isinstance(lain, File):
            return NotImplemented

        return (
            self.nama == lain.nama
            and self.pemilik == lain.pemilik
        )


class Dokumen(File):
    def __init__(self, nama, ukuran, pemilik, format="PDF"):
        super().__init__(nama, ukuran, pemilik)
        self.__format = format

    def baca(self):
        super().baca()
        return f"Membuka dokumen {self.nama} ({self.__format})"


class Gambar(File):
    def __init__(self, nama, ukuran, pemilik, resolusi="1920x1080"):
        super().__init__(nama, ukuran, pemilik)
        self.__resolusi = resolusi

    def info(self):
        return f"{self.nama} - resolusi {self.__resolusi}"


class Video(File):
    def __init__(self, nama, ukuran, pemilik, durasi=0):
        if (
            not isinstance(durasi, (int, float))
            or isinstance(durasi, bool)
            or durasi < 0
        ):
            raise ValidasiDataError(
                "Durasi video harus berupa angka positif"
            )

        super().__init__(nama, ukuran, pemilik)
        self.__durasi = durasi

    def info(self):
        return f"{self.nama} - durasi {self.__durasi} detik"


# ============================================================
# 4. CLASS FOLDER
# ============================================================

class Folder:
    def __init__(self, nama, pemilik):
        if not isinstance(nama, str) or not nama.strip():
            raise ValidasiDataError("Nama folder tidak boleh kosong")

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
            raise StrukturFolderError(
                "Isi folder harus berupa File atau Folder"
            )

        if item not in self.__isi:
            self.__isi.append(item)

    def buat_subfolder(self, nama):
        subfolder = Folder(nama, self.__pemilik)
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


# ============================================================
# 5. CLASS PENGGUNA
# ============================================================

class Pengguna:
    def __init__(self, username):
        if not isinstance(username, str) or not username.strip():
            raise ValidasiDataError("Username tidak boleh kosong")

        self.__username = username

    @property
    def username(self):
        return self.__username

    def buat_file(self, jenis, nama, ukuran, **kwargs):
        if jenis == "dokumen":
            return Dokumen(nama, ukuran, self, **kwargs)

        elif jenis == "gambar":
            return Gambar(nama, ukuran, self, **kwargs)

        elif jenis == "video":
            return Video(nama, ukuran, self, **kwargs)

        else:
            raise JenisFileError("Jenis file tidak dikenal")

    def buat_folder(self, nama):
        return Folder(nama, self)

    def akses_file(self, file):
        if not isinstance(file, File):
            raise ValidasiDataError("Objek yang diakses bukan file")

        if file.pemilik != self and not file.hak_akses.boleh_baca():
            raise AksesDitolakError("Akses ditolak")

        return file.baca()


# ============================================================
# 6. PROGRAM UTAMA
# ============================================================

def main():
    print("=== SISTEM MANAJEMEN FILE ===")

    try:
        # Membuat pengguna
        pemilik = Pengguna("purata")
        pengguna_lain = Pengguna("anon")

        print("\nPengguna berhasil dibuat")

        # Membuat folder
        folder = pemilik.buat_folder("Tugas Kuliah")

        # Membuat berbagai jenis file
        dokumen = pemilik.buat_file(
            "dokumen", "Laporan", 2.5, format="PDF"
        )

        gambar = pemilik.buat_file(
            "gambar", "Diagram", 1.2,
            resolusi="1920x1080"
        )

        video = pemilik.buat_file(
            "video", "Presentasi", 50, durasi=300
        )

        # Memasukkan file ke folder
        folder.tambah_item(dokumen)
        folder.tambah_item(gambar)
        folder.tambah_item(video)

        print("\n--- Isi Folder ---")
        print(folder.tampilkan_isi())

        # Membaca informasi file
        print("\n--- Informasi File ---")
        print(dokumen.baca())
        print(gambar.info())
        print(video.info())

        # Menguji validasi ukuran
        print("\n--- Pengujian Validasi ---")
        try:
            dokumen.ukuran = -5
        except ValidasiDataError as error:
            print("Validasi berhasil:", error)

        # Menguji jenis file tidak dikenal
        try:
            pemilik.buat_file("musik", "Lagu", 5)
        except SistemFileError as error:
            print("Jenis file:", error)

        # Menguji hak akses
        print("\n--- Pengujian Hak Akses ---")
        dokumen.hak_akses.ubah_izin(
            read=False,
            write=False
        )

        try:
            print(pengguna_lain.akses_file(dokumen))
        except AksesDitolakError as error:
            print("Akses ditolak:", error)

        # Menguji kesamaan file
        dokumen_duplikat = pemilik.buat_file(
            "dokumen", "Laporan", 2.5, format="PDF"
        )

        print("\n--- Informasi Tambahan ---")
        print("Dokumen sama:", dokumen == dokumen_duplikat)
        print("Jumlah file:", File.jumlah_file)
        print("Detail dokumen:", dokumen)

        # Membuat subfolder
        folder.buat_subfolder("Dokumen Tambahan")
        print(folder.tampilkan_isi())

    except SistemFileError as error:
        print("Terjadi kesalahan sistem:", error)

    except Exception as error:
        print("Terjadi kesalahan lain:", error)

    else:
        print("\nProgram berhasil dijalankan.")

    finally:
        print("\nProgram selesai.")


if __name__ == "__main__":
    main()
# ============================================================
# SISTEM MANAJEMEN FILE
# Gabungan dari:
# exceptions.py, hak_akses.py, file.py, folder.py,
# pengguna.py, dan main.py
# ============================================================


# ============================================================
# 1. CUSTOM EXCEPTIONS
# ============================================================

class SistemFileError(Exception):
    """Exception dasar untuk sistem manajemen file."""
    pass


class ValidasiDataError(SistemFileError, ValueError):
    """Terjadi ketika data tidak memenuhi aturan validasi."""
    pass


class AksesDitolakError(SistemFileError, PermissionError):
    """Terjadi ketika pengguna tidak memiliki izin."""
    pass


class JenisFileError(SistemFileError, ValueError):
    """Terjadi ketika jenis file tidak dikenal."""
    pass


class StrukturFolderError(SistemFileError, TypeError):
    """Terjadi ketika isi folder tidak valid."""
    pass


# ============================================================
# 2. CLASS HAK AKSES
# ============================================================

class HakAkses:
    def __init__(self, read=True, write=False):
        if not isinstance(read, bool) or not isinstance(write, bool):
            raise ValidasiDataError("Izin harus berupa boolean")

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
            raise ValidasiDataError("Izin harus berupa boolean")

        self.__read = read
        self.__write = write
        return "Hak akses berhasil diperbarui"


# ============================================================
# 3. CLASS FILE DAN TURUNANNYA
# ============================================================

class File:
    jumlah_file = 0

    def __init__(self, nama, ukuran, pemilik):
        if not self.validasi_nama(nama):
            raise ValidasiDataError("Nama file tidak valid")

        self.__nama = nama
        self.__ukuran = 0
        self.ukuran = ukuran
        self.__pemilik = pemilik
        self.__hak_akses = HakAkses()
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
        if not isinstance(nilai, (int, float)) or isinstance(nilai, bool):
            raise ValidasiDataError("Ukuran harus berupa angka")

        if nilai < 0:
            raise ValidasiDataError("Ukuran tidak boleh negatif")

        self.__ukuran = nilai

    @property
    def pemilik(self):
        return self.__pemilik

    @property
    def hak_akses(self):
        return self.__hak_akses

    def baca(self):
        if not self.__hak_akses.boleh_baca():
            raise AksesDitolakError("File tidak dapat dibaca")

        return f"Membaca file: {self.__nama}"

    def tulis(self, isi):
        if not self.__hak_akses.boleh_tulis():
            raise AksesDitolakError("Izin menulis ditolak")

        return f"Isi file {self.__nama} diperbarui"

    def info(self):
        return f"{self.__nama} ({self.__ukuran} MB)"

    def __str__(self):
        return f"{self.__nama} - {self.__ukuran} MB"

    def __eq__(self, lain):
        if not isinstance(lain, File):
            return NotImplemented

        return (
            self.nama == lain.nama
            and self.pemilik == lain.pemilik
        )


class Dokumen(File):
    def __init__(self, nama, ukuran, pemilik, format="PDF"):
        super().__init__(nama, ukuran, pemilik)
        self.__format = format

    def baca(self):
        super().baca()
        return f"Membuka dokumen {self.nama} ({self.__format})"


class Gambar(File):
    def __init__(self, nama, ukuran, pemilik, resolusi="1920x1080"):
        super().__init__(nama, ukuran, pemilik)
        self.__resolusi = resolusi

    def info(self):
        return f"{self.nama} - resolusi {self.__resolusi}"


class Video(File):
    def __init__(self, nama, ukuran, pemilik, durasi=0):
        if (
            not isinstance(durasi, (int, float))
            or isinstance(durasi, bool)
            or durasi < 0
        ):
            raise ValidasiDataError(
                "Durasi video harus berupa angka positif"
            )

        super().__init__(nama, ukuran, pemilik)
        self.__durasi = durasi

    def info(self):
        return f"{self.nama} - durasi {self.__durasi} detik"


# ============================================================
# 4. CLASS FOLDER
# ============================================================

class Folder:
    def __init__(self, nama, pemilik):
        if not isinstance(nama, str) or not nama.strip():
            raise ValidasiDataError("Nama folder tidak boleh kosong")

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
            raise StrukturFolderError(
                "Isi folder harus berupa File atau Folder"
            )

        if item not in self.__isi:
            self.__isi.append(item)

    def buat_subfolder(self, nama):
        subfolder = Folder(nama, self.__pemilik)
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


# ============================================================
# 5. CLASS PENGGUNA
# ============================================================

class Pengguna:
    def __init__(self, username):
        if not isinstance(username, str) or not username.strip():
            raise ValidasiDataError("Username tidak boleh kosong")

        self.__username = username

    @property
    def username(self):
        return self.__username

    def buat_file(self, jenis, nama, ukuran, **kwargs):
        if jenis == "dokumen":
            return Dokumen(nama, ukuran, self, **kwargs)

        elif jenis == "gambar":
            return Gambar(nama, ukuran, self, **kwargs)

        elif jenis == "video":
            return Video(nama, ukuran, self, **kwargs)

        else:
            raise JenisFileError("Jenis file tidak dikenal")

    def buat_folder(self, nama):
        return Folder(nama, self)

    def akses_file(self, file):
        if not isinstance(file, File):
            raise ValidasiDataError("Objek yang diakses bukan file")

        if file.pemilik != self and not file.hak_akses.boleh_baca():
            raise AksesDitolakError("Akses ditolak")

        return file.baca()


# ============================================================
# 6. PROGRAM UTAMA
# ============================================================

def main():
    print("=== SISTEM MANAJEMEN FILE ===")

    try:
        # Membuat pengguna
        pemilik = Pengguna("purata")
        pengguna_lain = Pengguna("anon")

        print("\nPengguna berhasil dibuat")

        # Membuat folder
        folder = pemilik.buat_folder("Tugas Kuliah")

        # Membuat berbagai jenis file
        dokumen = pemilik.buat_file(
            "dokumen", "Laporan", 2.5, format="PDF"
        )

        gambar = pemilik.buat_file(
            "gambar", "Diagram", 1.2,
            resolusi="1920x1080"
        )

        video = pemilik.buat_file(
            "video", "Presentasi", 50, durasi=300
        )

        # Memasukkan file ke folder
        folder.tambah_item(dokumen)
        folder.tambah_item(gambar)
        folder.tambah_item(video)

        print("\n--- Isi Folder ---")
        print(folder.tampilkan_isi())

        # Membaca informasi file
        print("\n--- Informasi File ---")
        print(dokumen.baca())
        print(gambar.info())
        print(video.info())

        # Menguji validasi ukuran
        print("\n--- Pengujian Validasi ---")
        try:
            dokumen.ukuran = -5
        except ValidasiDataError as error:
            print("Validasi berhasil:", error)

        # Menguji jenis file tidak dikenal
        try:
            pemilik.buat_file("musik", "Lagu", 5)
        except SistemFileError as error:
            print("Jenis file:", error)

        # Menguji hak akses
        print("\n--- Pengujian Hak Akses ---")
        dokumen.hak_akses.ubah_izin(
            read=False,
            write=False
        )

        try:
            print(pengguna_lain.akses_file(dokumen))
        except AksesDitolakError as error:
            print("Akses ditolak:", error)

        # Menguji kesamaan file
        dokumen_duplikat = pemilik.buat_file(
            "dokumen", "Laporan", 2.5, format="PDF"
        )

        print("\n--- Informasi Tambahan ---")
        print("Dokumen sama:", dokumen == dokumen_duplikat)
        print("Jumlah file:", File.jumlah_file)
        print("Detail dokumen:", dokumen)

        # Membuat subfolder
        folder.buat_subfolder("Dokumen Tambahan")
        print(folder.tampilkan_isi())

    except SistemFileError as error:
        print("Terjadi kesalahan sistem:", error)

    except Exception as error:
        print("Terjadi kesalahan lain:", error)

    else:
        print("\nProgram berhasil dijalankan.")

    finally:
        print("\nProgram selesai.")


if __name__ == "__main__":
    main()
