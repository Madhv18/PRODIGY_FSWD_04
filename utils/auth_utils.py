# file: utils/auth_utils.py
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token

def hash_password(plain: str) -> str:
    """Return a werkzeug-compatible PBKDF2 hash."""
    return generate_password_hash(plain)

def verify_password(plain: str, hashed: str) -> bool:
    """Verify the password against a werkzeug hash."""
    return check_password_hash(hashed, plain)

def generate_jwt(identity):
    return create_access_token(identity=identity)
