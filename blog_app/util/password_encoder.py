from django.contrib.auth.hashers import make_password, check_password



def encrypt_password(password):
    encrypted = make_password(password)
    return encrypted


def validate_password(new_password, original_password):
    check = check_password(new_password, original_password)
    return check