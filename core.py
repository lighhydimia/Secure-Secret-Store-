import os, json, base64
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet

def _derive_key_from_passphrase(passphrase: str, salt: bytes = None, iterations: int = 390000):
    from os import urandom
    if salt is None:
        salt = urandom(16)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=iterations,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(passphrase.encode()))
    return key, salt, iterations

def encrypt_json_obj(obj, passphrase):
    key, salt, iterations = _derive_key_from_passphrase(passphrase)
    f = Fernet(key)
    data = json.dumps(obj, ensure_ascii=False).encode('utf-8')
    token = f.encrypt(data)
    # return token and metadata
    payload = {
        "salt": base64.b64encode(salt).decode('ascii'),
        "iterations": iterations,
        "token": base64.b64encode(token).decode('ascii')
    }
    return payload

def decrypt_json_payload(payload, passphrase):
    salt = base64.b64decode(payload['salt'].encode('ascii'))
    iterations = int(payload.get('iterations', 390000))
    token = base64.b64decode(payload['token'].encode('ascii'))
    key, _, _ = _derive_key_from_passphrase(passphrase, salt=salt, iterations=iterations)
    f = Fernet(key)
    data = f.decrypt(token)
    obj = json.loads(data.decode('utf-8'))
    return obj
