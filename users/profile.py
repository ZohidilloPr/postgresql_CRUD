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


def ResetUserPassword(username, cursor, conn):
    """ user's password reset function """
    cursor.execute("SELECT id, username FROM users WHERE username = '%s';" % username)
    user_id = cursor.fetchone()[0]
    cursor.execute("SELECT users, question, answer FROM questions WHERE users = %i;" % user_id)
    questions = cursor.fetchall()
    print("*" * 50 + "\nif you want reset password, answer this questions: \n" + "*" * 50)
    print()
    correct, incorrect = [], []
    for question in questions: 
        print(question)
        print("Question 1: %s" % question[1])
        answer = input("Your Answer: ")
        if answer.lower() == question[2]:
            correct.append(answer)
        else:
            incorrect.append(answer)
    if int((len(questions) / 2) + 1) == len(correct):
        print("You answered enough to questions, Password resseting")
        for _ in range(3):
            password = input("Enter new password: ")
            password_1 = input("Enter new password again: ")
            if password == password_1:
                check = validate_password(password=password)
                if check["status"]:
                    password_encoding = encrypt_text(FERNET_GENERATE_KEY, password)
                    cursor.execute("UPDATE users SET password = '%s' WHERE id = %i;" % (password_encoding, user_id))
                    conn.commit()
                    print("Reseted Password")
                    break
                else:
                    print(check["error"])
            else:
                print("passwords are not same")
    elif int((len(questions) / 2) + 1) == len(incorrect):
        print("You didn't answered enough to questions")
        if input("do you try again ? (Y/n): ").lower() == "y":
            ResetUserPassword(username, cursor, conn)
    else:
        print("You didn't answered enough to questions")
        ResetUserPassword(username, cursor, conn)
