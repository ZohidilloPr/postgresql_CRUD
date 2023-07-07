import psycopg2
import platform
from users.login import Login
from views.add import WriteData
from views.read import ReadData
from config.settings import config
from users.register import Register
from terminaltables import AsciiTable
from config.data import creates_tables
from users.profile import ChangeUserPassword

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
        data = [["Names", "Values"],["Current User", user_login["username"]], ["Last Login", user_login["last_login"]], ["User PC", f"{platform.system()} {platform.release()}"], ["User PC OS version", platform.version()]]
        print()
        user_table = AsciiTable(data)
        user_table.inner_column_border = False
        print(user_table.table)
        print()
        if user_login["superuser"]:
            survey_start = input("Choice One: \n\t1. Read Data\n\t2. Write Data \n\t3. Register user\n\t4. Profile \nYour Option: ")
            if survey_start == "1":
                ReadData(cursor)
            elif survey_start == "2":
                WriteData(cursor, conn)
            elif survey_start == "3":
                Register(cursor, conn)
                Main()
            elif survey_start == "4":
                profile = input("Choice One: \n\t1. Change password \nYour Option: ")
                if profile == "1":
                    ChangeUserPassword(id=user_login["user_id"], cursor=cursor, conn=conn)

        elif user_login["staff"]:
            survey_start = input("Choice One: \n\t1. Read Data \n\t2.Profile \nYour Option: ")
            if survey_start == "1":
                ReadData(cursor)
            elif survey_start == "2":
                profile = input("Choice One: \n\t1. Change password \nYour Option: ")
                if profile == "1":
                    ChangeUserPassword(int(id=user_login["user_id"]), cursor=cursor, conn=conn)
    conn.close() # close database
Main()
