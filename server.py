from optparse import Option
import socket
import threading
from Compte import Compte, LireCompte, LireTousComptes, ModifierCompte, addCompte, authenticate
from Facture import LireFacture
from Transaction import EffectuerTransaction, LireTousTransactions

HEADER = 64
PORT = 5050
#SERVER = socket.gethostbyname(socket.gethostname())
SERVER = "192.168.1.16"
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

ANSWER_MESSAGE = "!ANSWER"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

connections = []
comptes = []


def send_message(conn, msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    conn.send(send_length)
    conn.send(message)


def recieve_msg(conn):
    send_message(conn, ANSWER_MESSAGE)
    msg_length = conn.recv(HEADER).decode(FORMAT)
    if msg_length:
        msg_length = int(msg_length)
        msg = conn.recv(msg_length).decode(FORMAT)
    return msg


def login(conn):
    msg = "Bienvenue ! Entrez votre numero de compte pour vous connectez"
    send_message(conn, msg)
    num_compte = recieve_msg(conn)
    num_compte.strip()
    msg = "entrez votre mot de passe SVP: "
    send_message(conn, msg)
    password = recieve_msg(conn)
    password.strip()
    if num_compte.lower() == "admin" and password.lower() == "admin":
        auth = {"status": True, 'data': "admin"}
    else:
        auth = authenticate(num_compte, password)
    print(f"{num_compte} - {password}")
    return auth


def lock(conn, compte):
    if compte.refCompte in comptes:
        msg = "Ce compte a une transaction en cours! Veuillez patientez!"
        send_message(conn, msg)
    while True:
        if compte.refCompte not in comptes:
            break
    comptes.append(compte.refCompte)


def unlock(compte):
    comptes.remove(compte.refCompte)


def send_menu(conn):
    option = '0'
    while option not in '12345':
        msg = "Que voulez vous faire ?"
        send_message(conn, msg)
        msg = "1 - Crediter votre Compte"
        send_message(conn, msg)
        msg = "2 - Debiter votre Compte"
        send_message(conn, msg)
        msg = "3 - Consulter votre Compte"
        send_message(conn, msg)
        msg = "4 - Consulter votre Facture"
        send_message(conn, msg)
        msg = "5 - Deconnectez-Vous"
        send_message(conn, msg)
        option = recieve_msg(conn)
        if option not in '1234':
            msg = "ERREUR: Choix Invalide!"
            send_message(conn, msg)
    return option


def send_admin_menu(conn):
    option = '0'
    while option not in '12345':
        msg = "Que voulez vous faire ?"
        send_message(conn, msg)
        msg = "1 - Consulter La liste Des Comptes"
        send_message(conn, msg)
        msg = "2 - Consulter la Facture d'un Compte"
        send_message(conn, msg)
        msg = "3 - Consulter l'historique de transactions"
        send_message(conn, msg)
        msg = "4 - Ajouter un compte"
        send_message(conn, msg)
        msg = "5 - Deconnectez-Vous"
        send_message(conn, msg)
        option = recieve_msg(conn)
        if option not in '1234':
            msg = "ERREUR: Choix Invalide!"
            send_message(conn, msg)
    return option


def handle_option(conn, compte, option):
    if option == '1':
        lock(conn, compte)
        msg = "Donnez le montant a ajouter ?"
        send_message(conn, msg)
        montant = int(recieve_msg(conn))
        while montant < 0:
            msg = "Vous devez introduire un montant positif"
            send_message(conn, msg)
            montant = int(recieve_msg(conn))
        operation = EffectuerTransaction(compte.refCompte, "ajout", montant)
        if operation == True:
            msg = f"Ajout de {montant}DT effectue avec success!"
        elif operation == False:
            msg = "ERREUR: Ajout Echoue! Reessayez !"
        send_message(conn, msg)
        unlock(compte)
    elif option == '2':
        lock(conn, compte)
        msg = "Donnez le montant a Debiter ?"
        send_message(conn, msg)
        montant = int(recieve_msg(conn))
        while montant < 0:
            msg = "Vous devez introduire un montant positif"
            send_message(conn, msg)
            montant = int(recieve_msg(conn))
        operation = EffectuerTransaction(compte.refCompte, "retrait", montant)
        if operation == True:
            msg = f"Retrait de {montant}DT effectue avec success!"
            send_message(conn, msg)
            facture = LireFacture(compte.refCompte)
            msg = "Votre Facture"
            send_message(conn, msg)
            send_message(conn, str(facture))
        else:
            msg = "ERREUR: Retrait Echoue! Vous avez depassez le plafond !"
            send_message(conn, msg)
        unlock(compte)
    elif option == '3':
        compte = LireCompte(compte.refCompte)
        send_message(conn, str(compte))
    elif option == '4':
        facture = LireFacture(compte.refCompte)
        send_message(conn, str(facture))


def handle_admin_option(conn, option):
    if option == '1':
        list_comptes = LireTousComptes()
        for compte in list_comptes:
            send_message(conn, str(compte))
    elif option == '2':
        msg = "Donnez le compte pour lequel vous voulez afficher la facture "
        send_message(conn, msg)
        ref = int(recieve_msg(conn))
        facture = LireFacture(ref)
        send_message(conn, str(facture))
    elif option == '3':
        liste_transactions = LireTousTransactions()
        for transction in liste_transactions:
            send_message(conn, str(transction))
    elif option == '4':
        msg = "Donnez l'identifian du compte "
        send_message(conn, msg)
        ref = int(recieve_msg(conn))
        msg = "Donnez le nom de l'utilisateur du compte "
        send_message(conn, msg)
        nom = recieve_msg(conn)
        msg = "Donnez le mot de passe du compte "
        send_message(conn, msg)
        password = recieve_msg(conn)
        msg = "Donnez le plafond du compte "
        send_message(conn, msg)
        plafond = recieve_msg(conn)
        etat = addCompte(ref, nom, password, plafond)
        if etat:
            msg = f"Compte {ref} Cree avec success"
        else:
            msg = "Donnes invalides ou l'identifiant du compte existe deja"
        send_message(conn, msg)


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    connected = True
    auth = login(conn)
    if auth['status']:
        compte = auth['data']
        try:
            send_message(conn, f"Bienvenue {auth['data'].name}")
        except:
            send_message(conn, f"Bienvenue {auth['data']}")
    else:
        send_message(
            conn, "Informations Invalides! Vous avez etes deconnecte!")
        send_message(conn, DISCONNECT_MESSAGE)
        connected = False
        connections.remove(conn)
        print(f"[{addr}] was disconnected due to invalid info!")
    while connected:
        if compte == 'admin':
            option = send_admin_menu(conn)
            if option == '5':
                send_message(conn, DISCONNECT_MESSAGE)
                connected = False
                connections.remove(conn)
                print(f"[{addr}] has disconnected!")
                break
            handle_admin_option(conn, option)
        else:
            option = send_menu(conn)
            if option == '5':
                send_message(conn, DISCONNECT_MESSAGE)
                connected = False
                connections.remove(conn)
                print(f"[{addr}] has disconnected!")
                break
            handle_option(conn, compte, option)
    conn.close()


def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        connections.append(conn)
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")


print("[STARTING] server is starting...")
start()
