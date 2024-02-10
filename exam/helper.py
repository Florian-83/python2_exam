import bcrypt

password = "r00t"
salt = b'$2b$12$9gSf/q99MmJ/.VHolBwTf.'

def hash_password(password):
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed

hash_password(password)

hashed = hash_password(password)