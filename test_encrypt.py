from modules.encryption import encrypt, decrypt

plain_text="password"
encoded=encrypt(plain_text)
decoded=decrypt(encoded)
print(plain_text)
print(isinstance(plain_text, str))
print(encoded)
print(str(decoded))
print(isinstance(decoded, str))
