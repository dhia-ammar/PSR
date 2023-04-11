from Compte import LireCompte, ModifierCompte
from Facture import ModifierFacture
from Cryptage import *
import os

dir = os.path.join(os.getcwd(), "Files")
transactions_file = os.path.join(dir, "Transactions.txt")


class Transaction:
    def __init__(self, refCompte, typeTransaction, valeur, etat="", resultat=""):
        self.refCompte = refCompte
        self.typeTransaction = typeTransaction
        self.valeur = str(valeur)
        self.etat = etat
        self.resultat = resultat

    def WriteFile(self):
        f = open(transactions_file, 'ab')
        data = str(self.refCompte) + '.' + self.typeTransaction + \
               '.' + self.valeur + '.' + self.etat + '.' + self.resultat
        encrypted_data = EncryptData('compteKey.key', str.encode(data))
        f.write(encrypted_data + str.encode('\n'))
        # print("Transaction est sauvegarder avec success")
        f.close()

    def __str__(self):
        info = "ID: " + str(self.refCompte) + "\n" + "Type de Transaction: " + \
               self.typeTransaction + "\n" + "Valeur: " + self.valeur + "\n" + "Resultat: " + self.resultat
        return info

    def AfficherTransaction(self):
        print("ID: " + str(self.refCompte))
        print("Type de Transaction: " + self.typeTransaction)
        print("Valeur: " + self.valeur)
        print("Resultat: " + self.resultat)


def LireTransactions(ref):
    f = open(transactions_file, 'rb')
    transactions = []
    while True:
        ligne = f.readline()
        if ligne == b'':
            break
        decryptedData = DecryptData('compteKey.key', ligne)
        data = decryptedData.split('.')
        transaction = Transaction(data[0], data[1], data[2], data[3], data[4])
        if int(transaction.refCompte) == ref:
            transactions.append(transaction)
    f.close()
    if len(transactions) == 0:
        raise Exception('Le compte naucun transaction')
    return transactions


def LireTousTransactions():
    f = open(transactions_file, 'rb')
    transactions = []
    for ligne in f.readlines():
        decryptedData = DecryptData('compteKey.key', ligne)
        data = decryptedData.split('.')
        # print(data)
        transaction = Transaction(data[0], data[1], data[2], data[3], data[4])
        transactions.append(transaction)
    f.close()
    return transactions


def EffectuerTransaction(refCompte, typeTransaction, montant):
    try:
        transaction = Transaction(refCompte, typeTransaction, montant)
        compte = LireCompte(refCompte)
        satuts = False
        if typeTransaction == "retrait" and (
                (compte.etat == "positif" and int(compte.plafond) + int(compte.valeur) < int(montant)) or (
                compte.etat == "negatif" and int(compte.plafond) - int(compte.valeur) < int(montant))):
            transaction.resultat = "echec"
            transaction.etat = compte.etat
            transaction.WriteFile()
        else:
            status = True
            oldEtat = compte.etat
            ModifierCompte(refCompte, typeTransaction, montant)
            transaction.resultat = "succees"
            compte = LireCompte(refCompte)
            transaction.etat = compte.etat
            transaction.WriteFile()
            if compte.etat == "negatif" and typeTransaction == "retrait":
                if compte.etat != oldEtat:
                    ModifierFacture(refCompte, int(compte.valeur))
                else:
                    ModifierFacture(refCompte, montant)
        return status
    except:
        print("Something Went Wrong")
