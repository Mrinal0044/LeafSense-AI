import bcrypt
# Monkeypatch to bypass passlib AttributeError: module 'bcrypt' has no attribute '__about__'
if not hasattr(bcrypt, "__about__") or not hasattr(bcrypt.__about__, "__version__"):
    class About:
        __version__ = getattr(bcrypt, "__version__", "4.0.0")
    bcrypt.__about__ = About()

# Monkeypatch bcrypt.hashpw to truncate password to 72 bytes to satisfy passlib checks
_original_hashpw = bcrypt.hashpw
def _patched_hashpw(password, salt):
    pwd_bytes = password.encode("utf-8") if isinstance(password, str) else password
    if len(pwd_bytes) > 72:
        pwd_bytes = pwd_bytes[:72]
    return _original_hashpw(pwd_bytes, salt)
bcrypt.hashpw = _patched_hashpw

from datetime import datetime, timedelta, timezone
from typing import Any, Union
from jose import jwt
from passlib.context import CryptContext
from app.core.config import settings

# Initialize password hashing context with bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify if a raw plain password matches its stored bcrypt hash.
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """
    Generate a secure bcrypt hash of a plain password.
    """
    return pwd_context.hash(password)

def create_access_token(subject: Union[str, Any], expires_delta: timedelta = None) -> str:
    """
    Generate a signed JWT Access Token containing subject details and expiration claims.
    """
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        
    to_encode = {
        "exp": expire,
        "sub": str(subject)
    }
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt
