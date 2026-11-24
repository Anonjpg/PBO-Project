from exceptions import ValidasiDataError


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