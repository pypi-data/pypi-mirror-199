from backend.settings import settings
from passlib.context import CryptContext

myctx = CryptContext(schemes=[settings.PASSWORD_HASHER])


class PasswordHasher:
    def hash_password(password: str) -> str:
        return myctx.hash(password)

    def verify_password(password: str, hash_pw: str) -> bool:
        return myctx.verify(password, hash_pw)
