from peewee import *

# ------------------------ Settings TCP -------------------------

TCP_HOST = '10.1.0.124'
TCP_PORT = 5000
MAX_TIMEOUT_ERRORS = 5
TPS_TIMEOUT = 4
FORMAT_DATE = "%d/%m/%y %H:%I"
ENCODING = "utf-8"
BYTE_ORDER = "little"
BUFFER_SIZE = 2


# -------------------------- Settings SQL ------------------------
# connexion à la BDD
mysql_db = MySQLDatabase(host='127.0.0.1', user='phpmyadmin', password='PassPass.', database='Fil_Rouge')
