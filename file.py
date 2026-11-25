
from hak_akses import HakAkses
from testPython.exceptions import ValidasiDataError, AksesDitolakError


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
        super().__init__(nama, ukuran, pemilik)

        if not isinstance(durasi, (int, float)) or isinstance(durasi, bool) or durasi < 0:
            raise ValidasiDataError("Durasi video harus berupa angka positif")

        self.__durasi = durasi

    def info(self):
        return f"{self.nama} - durasi {self.__durasi} detik"
