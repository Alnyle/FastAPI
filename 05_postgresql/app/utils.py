from datetime import datetime, timedelta, timezone

from fastapi import HTTPException, status
import jwt
from config import security_settings
from uuid import uuid4

from api.schemas import seller


def generate_access_token(
    data: dict, 
    expiry: timedelta = timedelta(seconds=1500)
) -> str:


    token = jwt.encode(
        payload={
            "user": {
                "name": data.get("user", {}).get("name"),
                "id": data.get("user", {}).get("id"),
                "jti": str(uuid4()),
            },
            "exp": datetime.now(timezone.utc) + expiry # set expiration date for the token
        },
        algorithm=security_settings.JWT_ALGORITHM,
        key=security_settings.JWT_SECRET
    )

    return token


def decode_access_token(token: str) -> dict:

    try: 
        return jwt.decode(
            jwt=token,
            key=security_settings.JWT_SECRET,
            algorithms=[security_settings.JWT_ALGORITHM]
        )

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired!"
        )
    except jwt.PyJWTError:
        return None
