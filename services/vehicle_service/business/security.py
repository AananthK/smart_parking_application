# security.py: module strictly for password handling

from passlib.context import CryptContext

# password hashing manager: chooses algorithm
pwd_context = CryptContext(
    schemes=["argon2", "bcrypt"],  # prefer argon2, allow bcrypt
    deprecated="auto",
)

# take a key and hash it with salting
def hash_key(key: str) -> str:
    return pwd_context.hash(key)

# compare a key to its hash to verify it
def verify_key(key: str, key_hash: str) -> bool:
    return pwd_context.verify(key, key_hash)
