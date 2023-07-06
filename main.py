import psycopg2
from users.login import Login
from views.add import WriteData
from views.read import ReadData
from config.settings import config
from users.register import Register
from config.data import creates_tables

# dasturdagi barcha funksialar toplanadigan file

params = config()
conn = psycopg2.connect(**params) # connecting database
cursor = conn.cursor()

def Main():
    """ ASOSIY FUNCTION """
    creates_tables(cursor, conn)
    user_login = Login(cursor, conn)
    if user_login:
        survey_start = input("Choice One: \n\t1. Read Data\n\t2. Write Data \nYour Option: ")
        if survey_start == "1":
            ReadData(cursor)
        elif survey_start == "2":
            WriteData(cursor, conn)
    else:
        pass
    conn.close() # close database
Main()
