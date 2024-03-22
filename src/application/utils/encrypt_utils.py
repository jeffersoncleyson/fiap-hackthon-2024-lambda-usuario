import hashlib


class EncryptUtils:

    def __init__(self) -> None:
        pass

    @staticmethod
    def encrypt(text: str):
        hash_object = hashlib.sha256(text.encode())
        return hash_object.hexdigest()
