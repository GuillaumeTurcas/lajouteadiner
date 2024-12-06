import os
import hashlib

def hash_password(password: str, salt: bytes = None, pepper: str = "default_pepper", iterations: int = 1000) -> dict:
    """
    Hash a password with SHA-512, including salt and pepper, with a specified number of iterations.
    
    Args:
        password (str): The password to hash.
        salt (bytes, optional): Salt to use for the hash. If None, a new salt is generated.
        pepper (str): A secret string added to the password before hashing (fixed).
        iterations (int): The number of hash iterations to perform.
    
    Returns:
        dict: A dictionary containing the salt and hashed password.
    """
    if salt is None:
        salt = os.urandom(16)  # Generate a 16-byte random salt

    # Combine password, salt, and pepper
    password_with_pepper = (password + pepper).encode()
    salted_password = salt + password_with_pepper

    # Perform the hashing with the specified number of iterations
    hash_result = salted_password
    for _ in range(iterations):
        hash_result = hashlib.sha512(hash_result).digest()

    return {
        "salt": salt.hex(),  # Return the salt in hexadecimal for easier storage
        "hash": hash_result.hex()  # Return the hash in hexadecimal
    }

# Example usage
password = "my_secure_password"
pepper = "my_secret_pepper"
result = hash_password(password, pepper=pepper)

print("Salt:", result["salt"])
print("Hash:", result["hash"])
