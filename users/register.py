
# register user view

COMMON_PASSWORDS = {
    "a123456",
    "123456a",
    "1234567",
    "1234567890",
    "iloveyou",
    "12345",
    "letmein123",
    "qwertyuiop",
    "123",
    "monkey",
    "dragon",
    "1234",
    "baseball",
    "superman",
    "helloworld",
    "qazwsx",
    "trustno1",
    "123qwe",
    "welcome123",
    "admin123",
    "password1234",
    "summer2022",
    "123abc!",
    "football123",
    "iloveyou123",
    "abc123!",
    "sunshine123",
}

MIN_PASSWORD_LENGTH = 5
MAX_PASSWORD_LENGTH = 50

def validate_password(password):
    """Password validation function"""
    if len(password) < MIN_PASSWORD_LENGTH:
        return {"status": False, "error": f"Password is too short. Minimum length is {MIN_PASSWORD_LENGTH}"}
    if len(password) > MAX_PASSWORD_LENGTH:
        return {"status": False, "error": f"Password is too long. Maximum length is {MAX_PASSWORD_LENGTH}"}
    if password in COMMON_PASSWORDS:
        return {"status": False, "error": "Password is too common"}
    if password.isdigit():
        return {"status": False, "error": "Password contains only numbers"}
    return {"status": True, "error": ""}


def Register(cursor):
    """Register new user"""
    cursor.execute("SELECT username FROM users;")
    usernames_list = [username[0] for username in cursor.fetchall()]
    print("\nAdd New User\n")
    username = "@" + input("Enter username: ").lower()
    if username not in usernames_list and username != "@":
        for check in range(3):
            password = input("Enter password: ")
            password_1 = input("Enter password again: ")
            if password != "" and password == password_1:
                if validate_password(password)["status"]:
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
                            break        
                        else:
                            if input(f"You didn't write 'true' or 'false'. You wrote: {superuser}.\nIf you want to change it, it will be set to 'false'.\nAre you agree? (Y/n): ").lower() == "y":
                                superuser = "FALSE"
                                break
                    sql = f"""
                        INSERT INTO users (f_name, l_name, username, password, staff, superuser)
                        VALUES ('{f_name}', '{l_name}', '{username}', '{password}', '{staff}', '{superuser}');
                    """
                    print(sql, "User registered successfully!")
                    break
                else:
                    print(validate_password(password)["error"])
            else:
                print("Passwords do not match. Please try again.")
    else:
        print("This username is already taken. Please choose a different username.")
        Register(cursor)

