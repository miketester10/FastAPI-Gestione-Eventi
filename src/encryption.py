import base64
import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from hashlib import sha256

from src.config import settings as s


class Encryption:
    __key = sha256(s.encryption_key.get_secret_value().encode()).digest()

    def encrypt(self, plaintext: str) -> str:
        iv = os.urandom(16)
        cipher = AES.new(self.__key, AES.MODE_CBC, iv)
        ciphertext = cipher.encrypt(pad(plaintext.encode(), AES.block_size))
        return base64.b64encode(iv + ciphertext).decode("utf-8")

    def decrypt(self, encrypted_text: str) -> str:
        raw_data = base64.b64decode(encrypted_text)
        iv = raw_data[:16]
        ciphertext = raw_data[16:]
        cipher = AES.new(self.__key, AES.MODE_CBC, iv)
        decrypted = unpad(cipher.decrypt(ciphertext), AES.block_size)
        return decrypted.decode("utf-8")


encryption = Encryption()
