from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=["argon2", "bcrypt"],
    deprecated="auto",
)

def hash_key(key: str) -> str:
    return pwd_context.hash(key)

def verify_key(key: str, key_hash: str) -> bool:
    return pwd_context.verify(key, key_hash)
