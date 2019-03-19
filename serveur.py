from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
import json
from peewee import DoesNotExist
from appli import analyse_message_recu
from models import GameServerConfig
from settings import TCP_HOST, TCP_PORT, BUFFER_SIZE, ENCODING, BYTE_ORDER

with socket(AF_INET, SOCK_STREAM) as sock:
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 2)
    sock.bind((TCP_HOST, TCP_PORT))
    sock.listen()
    print("Server listening at {}:{}".format(TCP_HOST, TCP_PORT))
    while True:
        (conn, addr) = sock.accept()
        addresse_ip = addr[0]
        print("Connection received from {}:{}".format(*addr))
        # lecture des 2 premiers bytes :
        msg_longueur = conn.recv(BUFFER_SIZE)
        length = (int.from_bytes(msg_longueur, byteorder=BYTE_ORDER))

        if length > 0:

            # je décode le message reçu, je le converti en str
            message_recu_str = conn.recv(length).decode(ENCODING)
            print("Received message: {}".format(message_recu_str))

            # je stock la réponse dans un dictionnaire
            message_recu_dict = json.loads(message_recu_str)

            if message_recu_dict.get('Msg type') == 'STATS':
                analyse_message_recu(message_recu_str, addresse_ip)
                message_reponse_dict = {"Msg type": "ACK", "Msg ID": message_recu_dict['Msg ID']}
                message_reponse_json = json.dumps(message_reponse_dict)
                message_bytes = bytes(str(message_reponse_json).encode(ENCODING))
                first_bytes = len(message_bytes).to_bytes(BUFFER_SIZE, byteorder=BYTE_ORDER)
                full_message = first_bytes + message_bytes
                conn.send(full_message)
                conn.close()
            elif message_recu_dict.get('Msg type') == 'CONFIG':
                try:
                    obj = GameServerConfig.get(GameServerConfig.name_server == message_recu_dict.get("Machine name"))
                    message_reponse_dict = {"Msg type": "CONFIG",
                                            "Msg ID": message_recu_dict['Msg ID'],
                                            "Max player delay": obj.max_player_delay,
                                            "Max coin blink delay": obj.max_coin_blink_delay,
                                            "Victory blink delay": obj.victory_blink_delay,
                                            "Level": obj.level,
                                            "Player1 color": obj.player1_color,
                                            "Player2 color": obj.player2_color,
                                            }
                except DoesNotExist:
                    message_reponse_dict = {}
                message_reponse_json = json.dumps(message_reponse_dict)
                message_bytes = bytes(str(message_reponse_json).encode(ENCODING))
                first_bytes = len(message_bytes).to_bytes(BUFFER_SIZE, byteorder=BYTE_ORDER)
                full_message = first_bytes + message_bytes
                conn.send(full_message)
                conn.close()
        else:
            print("Le serveur n'a renvoyé aucune réponse")
