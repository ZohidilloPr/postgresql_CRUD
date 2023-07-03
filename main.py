import psycopg2
from add import WriteData
from read import ReadData
from data import creates_tables
from config.settings import config

# dasturdagi barcha funksialar toplanadigan file

params = config()
conn = psycopg2.connect(**params) # connecting database
cursor = conn.cursor()


def Main():
    """ ASOSIY FUNCTION """
    creates_tables(cursor, conn)
    survey_start = input("Choice One: \n\t1. Read Data\n\t2. Write Data \nYour Option: ")
    
    if survey_start == "1":
        ReadData(cursor)
    
    elif survey_start == "2":
        WriteData(cursor, conn)

    # databaseni yopish uchun
    conn.close()

Main()