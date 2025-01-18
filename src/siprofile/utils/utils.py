import secrets
from hashlib import sha256


def generate_id(prefix: str = "id", nbytes: int = 6) -> str:
    random_id = secrets.token_hex(nbytes)
    return f"{prefix}-{random_id}"

def hash_password(password: str) -> str:
    return sha256(password.encode()).hexdigest()
