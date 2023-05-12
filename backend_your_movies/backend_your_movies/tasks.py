import environ
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
import os

env = environ.Env()

def get_private_key():
    private_key_path = os.path.join(os.path.dirname(__file__), '..', '..', 'private_key.pem')
    with open(private_key_path, 'rb') as f:
        encrypted_private_key = f.read()
        passphrase = env('PASSPHRASE')
        private_key = serialization.load_pem_private_key(
        encrypted_private_key,
        password=passphrase.encode(),
        backend=default_backend()
    )
    return private_key