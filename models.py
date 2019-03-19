from peewee import *
import datetime
import os
import json
from settings import mysql_db

mysql_db.connect()


class GameServerConfig(Model):
    adresse_ip = CharField(max_length=50, unique=True, )
    name_server = CharField(max_length=50, unique=True)
    game = CharField(max_length=50)
    max_player_delay = CharField(max_length=50, unique=True, default=12)
    max_coin_blink_delay = CharField(max_length=50, unique=True, default=12)
    victory_blink_delay = CharField(max_length=50,default=12)
    level = CharField(default=1)
    heure_modif = DateTimeField(default=datetime.datetime.now)
    player1_color = CharField(max_length=50, unique=True, default="blue")
    player2_color = CharField(max_length=50, unique=True, default="red")


    class Meta:
        database = mysql_db

    @classmethod
    def lister_serveur(cls):
        return cls.select()


class ReceivedMessage(Model):
    message = CharField(max_length=2000)
    message_ID = IntegerField()
    date_arrivee = DateTimeField(default=datetime.datetime.now)
    machine = ForeignKeyField(GameServerConfig, backref='ReceivedMessage')

    class Meta:
        database = mysql_db


class StatsPerMatch(Model):
    machine = ForeignKeyField(GameServerConfig, backref='StatsPerMatch')
    date_debut = DateTimeField()
    duree_jeu = IntegerField()
    gagnant = CharField()

    class Meta:
        database = mysql_db


class StatsPerDay(Model):
    date = DateField()
    machine = ForeignKeyField(GameServerConfig, backref='StatsPerDay')
    nb_partie_jour = IntegerField()
    duree_moy_partie_jour = IntegerField()
    nb_fois_gagnant1 = IntegerField()
    nb_fois_gagnant2 = IntegerField()
    nb_fois_egalite = IntegerField()

    class Meta:
        database = mysql_db


mysql_db.create_tables([GameServerConfig, ReceivedMessage, StatsPerMatch, StatsPerDay])

























