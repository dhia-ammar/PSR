from Cryptage import *
from Facture import Facture, LireFacture
import os


dir = os.path.join(os.getcwd(), "Files")
comptes_file = os.path.join(dir, "Comptes.txt")


class Compte:
    def __init__(self, refCompte, name, valeur, etat, plafond, password):
        self.name = name
        self.refCompte = int(refCompte)
        self.valeur = valeur
        self.etat = etat
        self.plafond = plafond
        self.password = password

    def WriteFile(self):
        f = open(comptes_file, 'ab')
        data = str(self.refCompte)+'.'+self.name+'.'+str(self.valeur) + \
            '.' + self.etat+'.'+str(self.plafond)+'.'+self.password
        encrypted_data = EncryptData('compteKey.key', str.encode(data))
        f.write(encrypted_data+str.encode('\n'))
        print("Compte est sauvegarder avec success")
        f.close()

    def __str__(self):
        info = "ID: "+str(self.refCompte)+"\n"+"Name: "+self.name+"\n"+"Valeur: " + \
            self.valeur+"\n"+"Etat: "+self.etat+"\n"+"Plafond: "+self.plafond
        return info

    def AfficherCompte(self):
        print("ID: "+str(self.refCompte))
        print("Name: "+self.name)
        print("Valeur: "+self.valeur)
        print("Etat: "+self.etat)
        print("Plafond: "+self.plafond)
        print("Password: "+self.password)


def LireCompte(ref):
    f = open(comptes_file, 'rb')
    while True:
        ligne = f.readline()
        if(ligne == b''):
            break
        decryptedData = DecryptData('compteKey.key', ligne)
        data = decryptedData.split('.')
        compte = Compte(data[0], data[1], data[2], data[3], data[4], data[5])
        if (int(compte.refCompte) == ref):
            return compte
    f.close()
    raise Exception("Le compte est introvable")


def LireTousComptes():
    f = open(comptes_file, 'rb')
    comptes = []
    while True:
        ligne = f.readline()
        if(ligne == b''):
            break
        decryptedData = DecryptData('compteKey.key', ligne)
        data = decryptedData.split('.')
        compte = Compte(data[0], data[1], data[2], data[3], data[4], data[5])
        comptes.append(compte)
    f.close()
    return comptes


def ModifierCompte(ref, type, montant):
    f = open(comptes_file, 'rb')
    existe = False
    comptes = []
    while True:
        ligne = f.readline()
        if(ligne == b''):
            break
        decryptedData = DecryptData('compteKey.key', ligne)
        data = decryptedData.split('.')
        print(len(data))
        compte = Compte(data[0], data[1], data[2], data[3], data[4], data[5])
        if (compte.refCompte == ref):
            existe = True
            if (type == "ajout"):
                print("ajout")
                if (compte.etat == "positif"):
                    print("positif")
                    compte.valeur = str(montant+int(compte.valeur))
                elif (compte.etat == "negatif"):
                    if(montant > int(compte.valeur)):
                        compte.valeur = str(montant-int(compte.valeur))
                        compte.etat = "positif"
                    else:
                        compte.valeur = str(int(compte.valeur)-montant)
            elif (type == "retrait"):
                if (compte.etat == "positif" and int(compte.plafond)+int(compte.valeur) < int(montant) or compte.etat == "negatif" and int(compte.plafond)-int(compte.valeur) < int(montant)):
                    raise Exception("Le solde de votre Compte est unsuffisent")
                elif(compte.etat == "negatif"):
                    compte.valeur = str(montant+int(compte.valeur))
                elif(compte.etat == "positif"):
                    if(montant > int(compte.valeur)):
                        compte.valeur = str(montant-int(compte.valeur))
                        compte.etat = "negatif"
                    else:
                        compte.valeur = str(int(compte.valeur)-montant)
            else:
                raise Exception("type de transaction est indefini")
        comptes.append(compte)
    f.close()
    if(not existe):
        raise Exception("Le compte Specifie est inrovable")
    # Clear the file
    f = open(comptes_file, 'w')
    f.close()
    print("lenArray:"+str(len(comptes)))
    for compte in comptes:
        compte.AfficherCompte()
        compte.WriteFile()
    print("Compte modifie avec success")


def EstExiste(refCompteRecherche):
    f = open(comptes_file, 'rb')
    while True:
        ligne = f.readline()
        print(ligne)
        # if(ligne == b''):
        if(ligne == ''):
            break
        decryptedData = DecryptData('compteKey.key', ligne)
        data = decryptedData.split('.')
        compte = Compte(data[0], data[1], data[2],
                        data[3], data[4], data[5])
        if (int(compte.refCompte) == int(refCompteRecherche)):
            return True
    f.close()
    return False


def addCompte(refCompte, name, password, plafond, valeur=0, etat="positif"):
    try:
        LireCompte(refCompte)
        LireFacture(refCompte)
        return False
    except:
        Compte(refCompte, name, valeur, etat, plafond, password).WriteFile()
        Facture(refCompte, 0).WriteFile()
        return True


def authenticate(refCompte, password):
    f = open(comptes_file, 'rb')
    resultat = dict()
    while True:
        ligne = f.readline()
        if(ligne == b''):
            break
        decryptedData = DecryptData('compteKey.key', ligne)
        data = decryptedData.split('.')
        compte = Compte(int(data[0]), data[1], data[2],
                        data[3], data[4], data[5])
        if (compte.refCompte == int(refCompte) and compte.password == password):
            resultat['status'] = True
            resultat['data'] = compte
            return resultat
    f.close()
    resultat['status'] = False
    return resultat

# addCompte("1000","nejah","nejah","500","400")
# addCompte("1001","dhia","nejah","500","400")
# addCompte("1002","siwar","nejah","500","400")
# addCompte("1003","rami","nejah","500","400")
# Compte("1000","nejah","200","positif","500","nejah").WriteFile()
# Compte("1001","rami","200","positif","500","nejah").WriteFile()
# Compte("1002","dhia","200","positif","500","nejah").WriteFile()
# Compte("1003","siwar","200","positif","500","nejah").WriteFile()
#ModifierCompte(1000, "retrait", 500)
# LireCompte(1003).AfficherCompte()
# compte.WriteFile()
# decryptedCompte=LireCompte(1002)
# print(decryptedCompte.name)
# comptes=LireTousComptes()
# print(len(comptes))
# name="nennnjah"
# encrypted=EncryptData('compteKey.key',name.encode())
# decrypted=DecryptData('compteKey.key',encrypted)
# print(decrypted)
# Compte("1004","nejah","200","positif","500","nejah").WriteFile()
