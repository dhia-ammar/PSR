from Cryptage import *
import os

dir = os.path.join(os.getcwd(), "Files")
factures_file = os.path.join(dir, "Factures.txt")


class Facture:
    def __init__(self, refCompte, somme):
        self.refCompte = refCompte
        self.somme = somme

    def AfficherFacture(self):
        print("ID: " + self.refCompte)
        print("Somme:" + self.somme)

    def __str__(self):
        info = "ID: " + self.refCompte + "\n" + "Somme:" + self.somme
        return info

    def WriteFile(self):
        f = open(factures_file, 'rb')
        while True:
            ligne = f.readline()
            if ligne == b'':
                break
            decryptedData = DecryptData('compteKey.key', ligne)
            data = decryptedData.split('.')
            facture = Facture(data[0], data[1])
            if (int(facture.refCompte) == int(self.refCompte)):
                raise Exception("La Facture est existe deja")
        f.close()
        f = open(factures_file, 'ab')
        data = str(self.refCompte) + '.' + str(self.somme)
        encrypted_data = EncryptData('compteKey.key', str.encode(data))
        f.write(encrypted_data + str.encode('\n'))
        # print("Facture est sauvegarder avec success")
        f.close()


def LireFacture(ref):
    f = open(factures_file, 'rb')
    existe = False
    for ligne in f.readlines():
        decryptedData = DecryptData('compteKey.key', ligne)
        data = decryptedData.split('.')
        facture = Facture(data[0], data[1])
        if int(facture.refCompte) == ref:
            existe = True
            return facture
    f.close()
    if not existe:
        raise Exception("La facture est intouvable")


def LireTousFactures():
    f = open(factures_file, 'rb')
    factures = []
    for ligne in f.readlines():
        decryptedData = DecryptData('compteKey.key', ligne)
        data = decryptedData.split('.')
        facture = Facture(data[0], data[1])
        factures.append(facture)
        facture.AfficherFacture()
    f.close()
    return factures


def ModifierFacture(ref, montant):
    f = open(factures_file, 'rb')
    factures = []
    existe = False
    for ligne in f.readlines():
        decryptedData = DecryptData('compteKey.key', ligne)
        data = decryptedData.split('.')
        facture = Facture(data[0], data[1])
        if (int(facture.refCompte) == ref):
            existe = True
            facture.somme = int(facture.somme) + int(montant * 0.02)
            # elif(type == "retrait"):
            # facture.somme = int(facture.somme)-montant
        factures.append(facture)
    f.close()
    if (not existe):
        raise Exception("Le compte Specifie est introuvable")
    # Clear the file
    f = open(factures_file, 'wb')
    f.close()
    for facture in factures:
        facture.WriteFile()
    print("Facture modifie avec success")

# Facture("1001",0).WriteFile()
# Facture("1002",0).WriteFile()
# Facture("1003",0).WriteFile()
# Facture("1004",0).WriteFile()
# LireFacture(1001).AfficherFacture()
# LireTousFactures()
# ModifierFacture(1001, "ajout", 100)
# LireTousFactures()
