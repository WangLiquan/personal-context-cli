from personal_context_cli.crypto import decrypt_payload, encrypt_payload


def test_encrypt_decrypt_roundtrip() -> None:
    payload = {"owner_profile": {"industry": "tech"}}
    token = encrypt_payload(payload, "pass123")
    restored = decrypt_payload(token, "pass123")
    assert restored == payload
