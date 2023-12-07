from cryptography.fernet import Fernet
from config import SECURITY_KEY

f=Fernet(SECURITY_KEY)

def encode(plaintext: str) -> str:
    return f.encrypt(plaintext.encode()).decode()

def decode(ciphertext: str) -> str:
    return f.decrypt(ciphertext.encode()).decode()