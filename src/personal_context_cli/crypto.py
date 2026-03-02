import base64
import json
from hashlib import scrypt

from cryptography.fernet import Fernet


def _derive_key(password: str, salt: bytes) -> bytes:
    key = scrypt(
        password=password.encode("utf-8"),
        salt=salt,
        n=2**14,
        r=8,
        p=1,
        dklen=32,
    )
    return base64.urlsafe_b64encode(key)


def encrypt_payload(data: dict, password: str) -> bytes:
    salt = b"local-fixed-salt-v1"
    fernet = Fernet(_derive_key(password, salt))
    raw = json.dumps(data, ensure_ascii=True).encode("utf-8")
    return fernet.encrypt(raw)


def decrypt_payload(token: bytes, password: str) -> dict:
    salt = b"local-fixed-salt-v1"
    fernet = Fernet(_derive_key(password, salt))
    raw = fernet.decrypt(token)
    return json.loads(raw.decode("utf-8"))
