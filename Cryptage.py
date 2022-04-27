from cryptography.fernet import Fernet


def GenerateKey(path):
    key = Fernet.generate_key()
    with open(path, 'wb') as filekey:
        filekey.write(key)


def GetKey(path):
    with open(path, 'rb') as filekey:
        return filekey.read()


def EncryptData(pathkey, data):
    key = GetKey(pathkey)
    fernet = Fernet(key)
    encrypted = fernet.encrypt(data)
    return encrypted


def DecryptData(path, data):
    key = GetKey(path)
    fernet = Fernet(key)
    decrypted = fernet.decrypt(data)
    return decrypted.decode()
