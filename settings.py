import peewee as pw
# ------------------------ Settings TCP -------------------------

TCP_HOST = '127.0.0.1'
TCP_PORT = 5000
MAX_TIMEOUT_ERRORS = 5
TPS_TIMEOUT = 4
FORMAT_DATE = "%d/%m/%y %H:%I"
ENCODING = "utf-8"
BYTE_ORDER = "little"
BUFFER_SIZE = 2


# -------------------------- Settings SQL ------------------------
# connexion à la BDD
mysql_db = pw.MySQLDatabase(host='10.1.0.126', user='equipeDavid', password='equipeDavid07210.', database='fil_rouge')
