from file import File
from exceptions import ValidasiDataError, StrukturFolderError


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