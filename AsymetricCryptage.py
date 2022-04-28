import rsa


def GenerateKeys():
    # Use at least 2048 bit keys nowadays, see e.g. https://www.keylength.com/en/4/
    publicKey, privateKey = rsa.newkeys(2048)
    # Export public key in PKCS#1 format, PEM encoded
    publicKeyPkcs1PEM = publicKey.save_pkcs1().decode('utf8')
    print(publicKeyPkcs1PEM)
    f = open('./public.pem', 'w')
    f.write(publicKeyPkcs1PEM)
    f.close()
    # Export private key in PKCS#1 format, PEM encoded
    privateKeyPkcs1PEM = privateKey.save_pkcs1().decode('utf8')
    print(privateKeyPkcs1PEM)
    f = open('./private.pem', 'w')
    f.write(privateKeyPkcs1PEM)
    f.close()
    # Save and load the PEM encoded keys as you like


# Import public key in PKCS#1 format, PEM encoded

# Import private key in PKCS#1 format, PEM encoded


def EncryptData(data):
    f = open('./public.pem', 'r')
    publicKey = f.read()
    f.close()
    publicKeyReloaded = rsa.PublicKey.load_pkcs1(publicKey.encode('utf8'))
    ciphertext = rsa.encrypt(str.encode(data), publicKeyReloaded)
    return ciphertext


def DecryptData(data):
    f = open('./private.pem', 'r')
    privateKey = f.read()
    f.close()
    privateKeyReloaded = rsa.PrivateKey.load_pkcs1(privateKey.encode('utf8'))
    decryptedMessage = rsa.decrypt(data, privateKeyReloaded)
    return decryptedMessage.decode('utf8')

# print (DecryptData(EncryptData("hello")))
