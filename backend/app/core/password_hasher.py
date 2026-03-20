import bcrypt

def hash_password(plain_password: str) -> str:
    # bcrypt automatically adds salt and hashes the password
    return bcrypt.hashpw(plain_password.encode(), bcrypt.gensalt()).decode()

def verify_password(plain_password: str, stored_hash: str) -> bool:
    # Compare the plain password against the stored hash
    return bcrypt.checkpw(plain_password.encode(), stored_hash.encode())