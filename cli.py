# coding: utf-8
"""

Client TCP
----------

Exécute un client TCP qui envoie des message de statistiques
et de demande de configuration sur le serveur passé en paramètres.


Arguments :

    * Adresse IP du server
    * Port d'écoute
    * Type de message à envoyer


Exemple d'utilisation :

    >> python tcp_client.py 192.168.0.45 5000 stats

"""

import argparse
from argparse import RawTextHelpFormatter
from datetime import datetime, timedelta
import json
import random
import socket
import time
import sys

BUFFER_SIZE = 2
MAX_TIMEOUT_ERRORS = 5
ENCODING = "utf-8"
BYTE_ORDER = "little"


def main(host, port, message_type):
    """

    Fonction principale du client TCP
    Ouvre une connexion sur le "host:port"
    et envoie au serveur des messages
    de type 'message' (stats ou config).

    Récupère la réponse du serveur et teste son contenu

    """

    # Vérifie que le type de message envoyé est bien 'config' ou 'stats'
    message_type = message_type.lower()
    if message_type not in MESSAGES:
        error("Le type de message n'est pas valide (choix disponibles : {})".format(" ou ".join(MESSAGES.keys())))
        sys.exit()

    # Récupère les fonctions selon le type de message en paramètre
    message_function, test_function = MESSAGES[message_type]
    errors_count = 0

    while True:
        message_dict = message_function()

        # Le dictionnaire python est converti en json
        message = json.dumps(message_dict)

        # Ouverture d'une connexion au socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            sock.settimeout(8)
            sock.connect((host, port))
        except (OSError, ConnectionRefusedError):
            print("Aucune connexion pour {}:{}".format(host, port))
            print("Nouvelle tentative dans quelques secondes...")
            errors_count += 1
        else:
            # Les 2 premier bytes du message envoyé contiennent la longueur de celui-ci
            # Ainsi, le serveur connait la longueur du message à recevoir
            errors_count = 0
            first_bytes = len(message).to_bytes(BUFFER_SIZE, byteorder=BYTE_ORDER)
            encoded_message = bytes(message.encode(ENCODING))
            full_message = first_bytes + encoded_message
            print("\n" + "-" * 80)
            print("Envoi d'un message de type '{}'".format(message_type))
            print("-" * 80)

            # Envoi du message
            sock.send(full_message)

            # Test de la réponse
            get_and_test_response(sock, test_function, message_dict)

        if errors_count >= MAX_TIMEOUT_ERRORS:
            error("Max timeout error")
            sys.exit()
        # On attend un instant avant d'envoyer un nouveau message
        time.sleep(random.randint(2, 4))


def get_and_test_response(s, test_function, init_message):
    """

    Récupère la réponse intégrale du client.
    Teste son contenu.
    Affiche des messages d'erreurs explicites en cas
    de non respect des spécifications.

     * s : socket
     * test_function : la fonction appelée pour
       tester la réponse

    """

    # On récupère d'abord les 2 premiers caractères contenant la longueur du message
    data = s.recv(BUFFER_SIZE)

    # Convertit les bytes en nombre entier
    # https://docs.python.org/fr/3.5/library/stdtypes.html#int.from_bytes
    length = int.from_bytes(data, byteorder=BYTE_ORDER)

    if length > 0:

        # Récupère ensuite le message dont la longueur est égale à 'length'
        response = s.recv(length)

        success("Le serveur a renvoyé une réponse : {}".format(response))
        test_first_bytes(data, length)
        test_function(response, init_message)
    else:
        error("Le serveur n'a renvoyé aucune réponse")


def error(msg):
    "Affiche un message rouge dans le terminal"
    print("\033[91m" + msg + "\033[0m")


def success(msg):
    "Affiche un message vert dans le terminal"
    print("\033[92m √ " + msg + "\033[0m")


def get_stat_message():
    """
    Retourne un dictionnaire de message
    statistiques d'une partie
    """
    start = datetime.now() - timedelta(minutes=4)
    end = datetime.now()
    date_format = "%d/%m/%y %H:%I"

    return {
        "Msg type": "STATS",
        "Msg ID": random.randint(9999, 99999),
        "Machine name": socket.gethostname(),
        "Game type": "morpion",
        "Start time": start.strftime(date_format),
        "End time": end.strftime(date_format),
        "Winner": random.choice(["player1", "player2"]),
    }


def test_stat_response(response, init_message):
    """
    Vérifie la réponse aux messages
    d'envoi de stats.
    """
    try:
        message = json.loads(response)
        if message == init_message:
            error("Le serveur a répété la réponse envoyée. Le serveur doit traiter la requête et envoyer une réponse correspondant aux spécifications")
            return
    except NameError:
        error("Le corps de la réponse n'est pas au format JSON")
        return

    try:
        msg_type = message["Msg type"]
        assert msg_type == "ACK"
        success("Le 'Msg type' est bien égal à 'ACK'")
    except (KeyError, AssertionError, TypeError):
        error("La réponse ne contient pas de 'Msg type' de type 'ACK'")
        return

    try:
        msg_id = message["Msg ID"]
        assert msg_id == init_message["Msg ID"]
        success("Le 'Msg ID' est bien égal au 'Msg ID' original'")
    except (KeyError, AssertionError):
        error("La réponse doit contenir un 'Msg ID' de la même valeur que le 'Msg ID' envoyé par le client.")
        return


def get_config_message():
    """
    Retourne un dictionnaire de message
    de demande de configuration du jeu
    """
    return {
        "Msg type": "CONFIG",
        "Msg ID": random.randint(9999, 99999),
        "Machine name": socket.gethostname(),
    }


def test_config_response(response, init_message):
    """
    Vérifie la réponse aux messages
    de demande de config
    """
    try:
        message = json.loads(response)
        if message == init_message:
            error("Le serveur a répété la réponse envoyée. Le serveur doit traiter la requête et envoyer une réponse correspondant aux spécifications")
            return
    except ValueError:
        error("Le corps de la réponse n'est pas au format JSON")
        return

    try:
        msg_type = message["Msg type"]
        assert msg_type == "CONFIG"
        success("Le 'Msg type' est bien égal à 'CONFIG'")
    except (KeyError, AssertionError):
        error("La réponse ne contient pas de 'Msg type' de type 'CONFIG'")
        return

    try:
        msg_id = message["Msg ID"]
        assert msg_id == init_message["Msg ID"]
        success("Le 'Msg ID' est bien égal au 'Msg ID' original'")
    except (KeyError, AssertionError):
        error("La réponse doit contenir un 'Msg ID' de la même valeur que le 'Msg ID' envoyé par le client.")
        return

    keys = [
        "Max player delay", "Max coin blink delay",
        "Victory blink delay", "Level", "Player1 color",
        "Player2 color"
    ]
    pass_tests = True
    for k in keys:
        if k not in message:
            pass_tests = False
            error("La réponse doit renvoyer une valeur pour \"{}\"".format(k))
    if pass_tests:
        success("Le réponse contient bien toutes les valeurs")


def test_first_bytes(first_bytes, length):
    """
    Vérifie que le serveur renvoie bien une réponse
    commençant par la longueur du message à lire.
    """
    try:
        assert "\\" in str(first_bytes)
        success("Les {} premiers bytes renvoyés par le serveur contiennent bien la longueur de la réponse".format(BUFFER_SIZE))
        success("Longueur du mesage à lire : {}".format(length))
    except (AssertionError, TypeError):
        error("Les {} premiers bytes renvoyés par le serveur doivent envoyer la longueur de la réponse.".format(BUFFER_SIZE))


MESSAGES = {
    "stats": [get_stat_message, test_stat_response],
    "config": [get_config_message, test_config_response],
}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="--------------------------------------------------------\n" +
                                     "Exécute un client TCP qui envoie des messages au serveur.\n" +
                                     "Passez l'adresse du serveur et le type de message en arguments.\n" +
                                     "Exemple : \n\n  >>> python tcp_client.py 192.168.0.45 5000 stats\n\n" +
                                     "--------------------------------------------------------",
                                     formatter_class=RawTextHelpFormatter)
    parser.add_argument('host', metavar='h', type=str, help="L'adresse IP du serveur (par ex : 192.168.0.45)")
    parser.add_argument('port', metavar='p', type=int, help="Le port TCP du serveur (par ex : 5000)")
    parser.add_argument('message_type', metavar='m', type=str, help="Type de message à envoyer ('stats' ou 'config')")
    args = {k: v for k, v in vars(parser.parse_args()).items() if v is not None}
    main(**args)
