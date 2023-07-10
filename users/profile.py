from config.settings import FERNET_GENERATE_KEY
from .utilits import (validate_password, decrypt_text, encrypt_text)
# user profile view

def ChangeUserPassword(id, cursor, conn):
    """ user change password in this function """
    cursor.execute("SELECT id, username, password FROM users WHERE id = %i;" %id) # get user who using program.
    user = cursor.fetchone() # gather data
    decript_password = str(decrypt_text(FERNET_GENERATE_KEY, str(user[2]).encode("utf-8"))) # decode password and convert to string
    for _ in range(3):
        old_password = input("Enter old password: ") # get old password
        if old_password == decript_password: # check old passwords 
            for _ in range(3):
                new_password = input("Enter new password: ")
                new_password_1 = input("Enter new password again: ")
                if new_password == new_password_1: # check samely test
                    check = validate_password(password=new_password) # password validation
                    if check["status"]:
                        password = encrypt_text(FERNET_GENERATE_KEY, new_password) # password encoding
                        cursor.execute("UPDATE users SET password = '%s' WHERE id = %d;" % (password, id)) # prepare sql query
                        conn.commit() # update password
                        print("changed pasword")
                        break
                    else:
                        print(check["error"])
                else:
                    print("Passwords is not same")
            break
        else:
            print("Password is incorrect !")


def ResetUserPassword():
    """ user's password reset function """