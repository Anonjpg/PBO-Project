
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
