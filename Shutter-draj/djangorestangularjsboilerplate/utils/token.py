import hashlib
import random

def generate(email):
    '''
    The activation key for the ``UserStatus`` will be a
    SHA1 hash, generated from a combination of the ``User``'s
    email and a random salt.
    '''
    salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
    if isinstance(email, unicode):
        email = email.encode('utf-8')
    token = hashlib.sha1(salt+email).hexdigest()

    return token
