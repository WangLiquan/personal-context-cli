from pathlib import Path

from .crypto import decrypt_payload, encrypt_payload


class EncryptedStore:
    def __init__(self, path: Path):
        self.path = path

    def save(self, data: dict, password: str) -> None:
        self.path.write_bytes(encrypt_payload(data, password))

    def load(self, password: str) -> dict:
        return decrypt_payload(self.path.read_bytes(), password)
