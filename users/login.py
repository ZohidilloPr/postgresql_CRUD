from datetime import datetime
from .utilits import decrypt_text
from cryptography.fernet import Fernet
from .profile import ResetUserPassword
from config.settings import FERNET_GENERATE_KEY

# users login views


def Login(cursor, conn):
    """ user login system """
    date = datetime.now()
    username = "@" + input("Enter username @: ").lower()
    cursor.execute(f"SELECT id, username, password, staff, superuser, last_login FROM users WHERE username = '{username}';")
    get_user = cursor.fetchone()
    if get_user != None:
        for _ in range(3):
            password = input("Enter password: ")
            if _ == 1 and input("did you forget password ? (Y/n): ").lower() == "y":
                ResetUserPassword(username=username, cursor=cursor, conn=conn)
            if username == "@guest":
                if password == "guest":
                    sql = f"UPDATE users SET last_login = TIMESTAMP '{date}' WHERE id = 1;"
                    cursor.execute(sql)
                    conn.commit()  
                    return {"status": True, "user_id": get_user[0], "staff": True, "superuser": False, "username": username, "last_login": get_user[5], "user_status": "superuser" if get_user[4] else "usermassan" "staff" if get_user[3] else "usermassan"}
            else:
                password_decode = str(decrypt_text(FERNET_GENERATE_KEY, str(get_user[2]).encode("utf-8")))
                if password == password_decode:
                    sql = f"UPDATE users SET last_login = TIMESTAMP '{date}' WHERE id = {get_user[0]};"
                    cursor.execute(sql)
                    conn.commit()  
                    return {"status": True, "user_id": get_user[0], "staff": get_user[3], "superuser": get_user[4], "username": get_user[1], "last_login": get_user[5], "user_status": "superuser" if get_user[4] else "usermassan" "staff" if get_user[3] else "usermassan"}
                else:
                    print("password is invalid")
    else:
        print("username is not found")
        Login(cursor, conn)

