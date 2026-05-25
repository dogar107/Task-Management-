from fastapi import HTTPException, Header
import jwt
from jwt.exceptions import PyJWTError, ExpiredSignatureError
from src.utils.settings import settings

def isauthenticated(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="No token provided")

    parts = authorization.split(" ")

    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(status_code=401, detail="Invalid token format")

    token = parts[1]

    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )

        return {"id": payload["id"]}  

    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")

    except PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")