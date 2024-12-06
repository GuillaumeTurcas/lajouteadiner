import os
import hashlib
from security_config.secret_data import pepper, iterations

def hash_password(password: str, salt: bytes = None) -> str:

    # Combine password, salt, and pepper
    password_with_pepper = (password + pepper).encode()
    salted_password = salt + password_with_pepper

    # Perform the hashing with the specified number of iterations
    hash_result = salted_password
    for _ in range(iterations):
        hash_result = hashlib.sha512(hash_result).digest()

    return hash_result.hex()
