""" from werkzeug.security import safe_str_cmp
from auth import Auth
from user import User

def authenticate(username, password):
    user = Auth.find_by_name(username)
    if user and User.check_encrypted_password(password,user.password):
        return user


def identity(payload):
    user_id = payload['identity']
    return Auth.find_by_id(user_id) """