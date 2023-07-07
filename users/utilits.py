from cryptography.fernet import Fernet
# utilits for users functions

def encrypt_text(key, text):
    """ text encripting function """
    cipher_suite = Fernet(key)
    encrypted_text = cipher_suite.encrypt(text.encode('utf-8'))
    return encrypted_text.decode("utf-8")


def decrypt_text(key, encrypted_text):
    """ decode text function """
    cipher_suite = Fernet(key)
    decrypted_text = cipher_suite.decrypt(encrypted_text).decode('utf-8')
    return decrypted_text


def validate_password(password):
    """Password validation function"""

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

    if len(password) < MIN_PASSWORD_LENGTH:
        return {"status": False, "error": f"Password is too short. Minimum length is {MIN_PASSWORD_LENGTH}"}
    if len(password) > MAX_PASSWORD_LENGTH:
        return {"status": False, "error": f"Password is too long. Maximum length is {MAX_PASSWORD_LENGTH}"}
    if password in COMMON_PASSWORDS:
        return {"status": False, "error": "Password is too common"}
    if password.isdigit():
        return {"status": False, "error": "Password contains only numbers"}
    return {"status": True, "error": ""}