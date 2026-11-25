from file import File, Dokumen, Gambar, Video
from folder import Folder
from exceptions import (
    ValidasiDataError,
    JenisFileError,
    AksesDitolakError
)


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