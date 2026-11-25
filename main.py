from pengguna import Pengguna
from file import File
from exceptions import (
    SistemFileError,
    AksesDitolakError,
    ValidasiDataError
)


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