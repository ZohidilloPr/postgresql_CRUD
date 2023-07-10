from terminaltables import AsciiTable
from config.settings import FERNET_GENERATE_KEY
from .utilits import validate_password, encrypt_text

# register user view

def CommanQuestion(user_id, cursor, conn):
    """ questions are for reset users's password """
    time = 1
    while True:
        cursor.execute("SELECT id, users, question FROM questions WHERE users = %d;" % user_id)
        q = cursor.fetchall()
        data = [{que[2]} for que in q] # making list for selected questions
        selected_questions = [que[2] for que in q] # making list for cheking selected list
        data.insert(0, ["Question"]) 
        if len(data) == 6:
            print("All Answers saved successfully :)")
            break
        else:
            if len(data) != 1:
                print("You selected questions: ")
                table = AsciiTable(data)
                print(table.table)
            table_header = [["Question Id", "Question"]]
            questions = {
                "1": "What is your birth place name ?",
                "2": "What is your first book name ?",
                "3": "What is your first pet name ?",
                "4": "Where is your parent`s birth place ?",
                "5": "What is your superhero name ?"
            }
            print("\nChoice your question: ")
            for q in questions:
                if questions[q] not in selected_questions: # check questions what it was selected
                    table_header.append(["%s" % q, "%s" % questions[q]])
            table = AsciiTable(table_header)
            print(table.table)
            try:
                questions_id = input("\nEnter question id: ")
                if questions_id == "end":
                    print("All Answers saved successfully :)")
                    break
                if questions[questions_id] not in selected_questions:
                    answer = input("Your Answer: ").lower()
                    sql = """
                        INSERT INTO questions (users, question, answer)
                        VALUES (%i, '%s', '%s');
                    """ % (user_id, questions[questions_id], answer)
                    cursor.execute(sql) # prepare sql query
                    conn.commit() # push sql query to posrgesql
                    if input("If you want to add questions again ? (Y/n): ").lower() == "y":
                        time += 1
                        continue
                    else:break
                else:
                    print("Sorry, This questions already taken !")
            except Exception as e:
                print("Error: Maybe You entered incorrect value. \nPlease Check and try again")
                print("if you want to end this app, Write 'end' on 'questions id' field")
                

def Register(cursor, conn):
    """Register new user"""
    cursor.execute("SELECT username FROM users;") # get only usernames
    usernames_list = [username[0] for username in cursor.fetchall()] # convert to list
    print("\nAdd New User\n")
    username = "@" + input("Enter username: ").lower()
    if username not in usernames_list and username != "@": # checking username
        for check in range(3):
            password = input("Enter password: ")
            password_1 = input("Enter password again: ")
            if password != "" and password == password_1: # checking password
                if validate_password(password)["status"]: # validating password
                    password_encode = encrypt_text(FERNET_GENERATE_KEY, password)
                    f_name = input("Enter first name: ")
                    l_name = input("Enter last name: ")
                    for _ in range(3):
                        print("Staff user is a user who has limited permissions and can only read data.")
                        staff = input("Is the user a staff member? Write only (true/false): ").upper()
                        if staff == "TRUE" or staff == "FALSE":
                            break
                        else:
                            if input(f"You didn't write 'true' or 'false'. You wrote: {staff}.\nIf you want to change it, it will be set to 'false'.\nAre you agree? (Y/n): ").lower() == "y":
                                staff = "FALSE"
                                break
                            else:
                                continue
                    for _ in range(3):
                        print("Superuser is a user who has all permissions and can perform all actions in the program.")
                        superuser = input("Is the user a superuser? Write only (true/false): ").upper()
                        if superuser == "TRUE" or superuser == "FALSE":
                            if superuser == "TRUE" and staff == "FALSE":
                                staff = "TRUE"
                            break        
                        else:
                            if input(f"You didn't write 'true' or 'false'. You wrote: {superuser}.\nIf you want to change it, it will be set to 'false'.\nAre you agree? (Y/n): ").lower() == "y":
                                superuser = "FALSE"
                                break
                    sql = f"""
                        INSERT INTO users (f_name, l_name, username, password, staff, superuser)
                        VALUES ('{f_name}', '{l_name}', '{username}', '{password_encode}', '{staff}', '{superuser}');
                    """
                    cursor.execute(sql) # prepeir sql query
                    conn.commit() # push data to postgresql
                    print("User registered successfully!\n")
                    cursor.execute("SELECT id FROM users WHERE username = '%s';" % (username))
                    current_user = cursor.fetchone()
                    print("This questions will help when \nif You forget your password, you can reset password with this questions. \n")
                    CommanQuestion(user_id=current_user[0], cursor=cursor, conn=conn)    
                    break
                else:
                    print(validate_password(password)["error"])
            else:
                print("Passwords do not match. Please try again.")
    else:
        print("This username is already taken. Please choose a different username.")
        Register(cursor, conn)

