from models import *

class File_recup:

    def __init__(self, json_formatted_string, addresse_ip):
        dico = json.loads(json_formatted_string)
        self.msg_type = dico["Msg type"]
        self.msg_id = dico["Msg ID"]
        self.machine_name = dico["Machine name"]
        self.game_type = dico["Game type"]
        self.winner = dico["Winner"]
        self.day_date = datetime.datetime.strptime(dico["Start time"], "%d/%m/%y %H:%M").date()
        self.game_start = datetime.datetime.strptime(dico["Start time"], "%d/%m/%y %H:%M")
        self.game_end = datetime.datetime.strptime(dico["End time"], "%d/%m/%y %H:%M")
        self.json_formatted_string = json_formatted_string
        try:
            self.machine = GameServerConfig.get(GameServerConfig.name_server == self.machine_name)
        except DoesNotExist:
            self.machine = GameServerConfig.create(adresse_ip=addresse_ip,
                                                   name_server=self.machine_name,
                                                   game='Puissance4',
                                                   max_player_delay=10,
                                                   max_coin_blink_delay=1,
                                                   victory_blink_delay=1,
                                                   level=1,
                                                   heure_modif=datetime.datetime.now(),
                                                   player2_color='rouge',
                                                   player1_color='jaune')

    def get_winner(self):
        return self.winner

    def get_day(self):
        return self.day_date

    def get_game_duration(self):
        duration = self.game_end - self.game_start
        return duration.total_seconds()

    def get_server(self):
        return self.machine

def analyse_message_recu(message_str, addr):
    my_analyser = File_recup(message_str, addr)

    # METHODE Received Message
    ReceivedMessage.get_or_create(message=my_analyser.json_formatted_string,
                                  message_ID=my_analyser.msg_id,
                                  machine=my_analyser.machine)

    # METHODE Statistiques par Partie :
    StatsPerMatch.get_or_create(machine=my_analyser.machine, date_debut=my_analyser.day_date,
                                duree_jeu=my_analyser.get_game_duration(), gagnant=my_analyser.winner)

    # METHODE Statistiques par Jour:
    try:
        obj = StatsPerDay.get(StatsPerDay.machine == my_analyser.get_server(),
                              StatsPerDay.date == my_analyser.get_day())
        obj.nb_partie_jour += 1
        obj.duree_moy_partie_jour += my_analyser.get_game_duration()
        if my_analyser.get_winner() == 'player1':
            obj.nb_fois_gagnant1 += 1
        elif my_analyser.get_winner() == 'player2':
            obj.nb_fois_gagnant2 += 1
        else:
            obj.nb_fois_egalite += 1
        obj.save()

    except DoesNotExist:
        if my_analyser.get_winner() == 'player1':
            gagnant_is_player1 = 1
            gagnant_is_player2 = 0
            egalite = 0
        elif my_analyser.get_winner() == 'player2':
            gagnant_is_player1 = 1
            gagnant_is_player2 = 0
            egalite = 0
        else:
            gagnant_is_player1 = 0
            gagnant_is_player2 = 0
            egalite = 1
        StatsPerDay.create(date=my_analyser.get_day(),
                           machine=my_analyser.get_server(),
                           nb_partie_jour=1,
                           duree_moy_partie_jour=my_analyser.get_game_duration(),
                           nb_fois_gagnant1=gagnant_is_player1,
                           nb_fois_gagnant2=gagnant_is_player2,
                           nb_fois_egalite=egalite)


