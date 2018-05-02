import base64
import hashlib
import uuid


def generate_salt():
    return uuid.uuid4()


def hash_password(password, salt):
    password = password.encode('utf-8')
    return hashlib.sha512(password + salt.bytes).hexdigest()
