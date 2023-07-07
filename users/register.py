from config.settings import FERNET_GENERATE_KEY
from .utilits import validate_password, encrypt_text

# register user view

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
                    print("User registered successfully!")
                    break
                else:
                    print(validate_password(password)["error"])
            else:
                print("Passwords do not match. Please try again.")
    else:
        print("This username is already taken. Please choose a different username.")
        Register(cursor, conn)

