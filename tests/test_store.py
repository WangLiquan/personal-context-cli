from pathlib import Path

from personal_context_cli.store import EncryptedStore


def test_store_writes_encrypted_file_only(tmp_path: Path) -> None:
    store = EncryptedStore(tmp_path / "profile.enc")
    store.save({"owner_profile": {"age": 30}}, "pass123")
    assert (tmp_path / "profile.enc").exists()
    assert not (tmp_path / "profile.json").exists()
