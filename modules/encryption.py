from cryptography.fernet import Fernet
import os
from dotenv import load_dotenv

load_dotenv()
key = os.getenv("SECURITY_KEY").encode("UTF-8")
f = Fernet(key)


def encrypt(text: str) -> str:
    return f.encrypt(text.encode("UTF-8")).decode("UTF-8")


def decrypt(text: str) -> str:
    return f.decrypt(text.encode("UTF-8")).decode("UTF-8")
