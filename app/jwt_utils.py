# app/jwt_utils.py
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any
from jose import jwt
from config import JWT_SECRET, JWT_ALGORITHM, JWT_EXPIRES_MINUTES

def create_access_token(subject: str, extra_claims: Optional[Dict[str, Any]] = None) -> str:
    """
    subject = uid user.
    Token berlaku JWT_EXPIRES_MINUTES menit (UTC).
    """
    now = datetime.now(timezone.utc)
    exp = now + timedelta(minutes=JWT_EXPIRES_MINUTES)

    payload: Dict[str, Any] = {
        "sub": subject,                   # siapa pemilik token
        "iat": int(now.timestamp()),      # issued-at
        "exp": int(exp.timestamp()),      # expiry
    }
    if extra_claims:
        payload.update(extra_claims)

    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
