# app/security.py
from passlib.context import CryptContext

# konfigurasi passlib: gunakan bcrypt
_pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(plain_password: str) -> str:
    """
    Menghasilkan hash dari password plaintext.
    Simpan HASIL fungsi ini ke kolom users.passwordHash (bukan plaintext).
    """
    return _pwd.hash(plain_password)

def verify_password(plain_password: str, password_hash: str) -> bool:
    """
    Memverifikasi apakah plaintext cocok dengan hash yang disimpan.
    """
    return _pwd.verify(plain_password, password_hash)
