import psycopg2
import platform
from users.login import Login
from views.add import WriteData
from views.read import ReadData
from config.settings import config
from users.register import Register
from terminaltables import AsciiTable
from config.data import creates_tables
# dasturdagi barcha funksialar toplanadigan file

params = config()
conn = psycopg2.connect(**params) # connecting database
cursor = conn.cursor()

print()
print("If you have not account, You can enter as guest")
print("***But You can only read data.")
print("Username: guest\nPassword: guest")
print()

def Main():
    """ ASOSIY FUNCTION """
    creates_tables(cursor, conn)
    user_login = Login(cursor, conn)
    if user_login["status"]:
        data = [["Current User", "Last Login", "User PC", "User PC OS version"], [user_login["username"], user_login["last_login"], f"{platform.system()} {platform.release()}", platform.version()]]
        print()
        user_table = AsciiTable(data)
        user_table.inner_column_border = False
        print(user_table.table)
        print()
        if user_login["superuser"]:
            survey_start = input("Choice One: \n\t1. Read Data\n\t2. Write Data \n\t3. Register user\nYour Option: ")
            if survey_start == "1":
                ReadData(cursor)
            elif survey_start == "2":
                WriteData(cursor, conn)
            elif survey_start == "3":
                Register(cursor, conn)
        elif user_login["staff"]:
            survey_start = input("Choice One: \n\t1. Read Data \nYour Option: ")
            if survey_start == "1":
                ReadData(cursor)

    conn.close() # close database
Main()


"""
import sys
if sys.stdout.isatty():
    print("Inside a terminal!")
else:
    print("Piped output")
"""