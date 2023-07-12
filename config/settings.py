from decouple import config as conn
from configparser import ConfigParser

# encode and decode password fernet key
FERNET_GENERATE_KEY = conn("FERNET_GENERATE_KEY").encode("utf-8")

def config():
    """ .env filedan malumotlarni olish uchun """
    database = {
        "host": conn("host"),
        "dbname": conn("dbname"),
        "user": conn("user"),
        "password": conn("password"),
        "port": conn("port")
    }
    return database