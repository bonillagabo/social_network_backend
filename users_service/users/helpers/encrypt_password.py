import hashlib


def hash_md5(password):
    pass_to_hash = str(password).encode("utf-8")
    hash_md5 = hashlib.md5(pass_to_hash).hexdigest()
    return hash_md5
