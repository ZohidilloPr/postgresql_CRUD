from datetime import datetime
from cryptography.fernet import Fernet
# users login views

FERNET_GENERATE_KEY = b'sZ0MqyVScIA44tlap-N0FIbD11FSCXlgxyoomRCS2O4='


def decrypt_text(key, encrypted_text):
    """ decode text function """
    cipher_suite = Fernet(key)
    decrypted_text = cipher_suite.decrypt(encrypted_text).decode('utf-8')
    return decrypted_text


def Login(cursor, conn):
    """ user login system """
    date = datetime.now()
    username = "@" + input("Enter username @: ").lower()
    cursor.execute(f"SELECT id, username, password FROM users WHERE username = '{username}';")
    get_user = cursor.fetchone()
    if get_user != None:
        for _ in range(3):
            password = input("Enter password: ")
            if username == "@guest":
                if password == "guest":
                    sql = f"UPDATE users SET last_login = TIMESTAMP '{date}' WHERE id = 1;"
                    cursor.execute(sql)
                    conn.commit()  
                    return True
            else:
                password_decode = str(decrypt_text(FERNET_GENERATE_KEY, str(get_user[2]).encode("utf-8")))
                if password == password_decode:
                    sql = f"UPDATE users SET last_login = TIMESTAMP '{date}' WHERE id = {get_user[0]};"
                    cursor.execute(sql)
                    conn.commit()  
                    return True
                else:
                    print("password is invalid")
    else:
        print("username is not found")
        Login(cursor, conn)


def user_is_authenticated(user_login):
    """ check user is authenticated """
