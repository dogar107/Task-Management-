import jwt
from fastapi import HTTPException, Request
from datetime import datetime, timedelta
from pwdlib import PasswordHash
from sqlalchemy.orm import Session

from src.users.models import UserModel
from src.users.dtos import UserSchema, LoginSchema
from src.utils.settings import settings

password_hash = PasswordHash.recommended()


def hash_password(password: str):
    return password_hash.hash(password)


def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)


def login_user(body: LoginSchema, db: Session):

    user = db.query(UserModel).filter(
        UserModel.username == body.username
    ).first()

    if not user:
        raise HTTPException(status_code=400, detail="Login not found")

    if not verify_password(body.password, user.password):
        raise HTTPException(status_code=400, detail="Wrong password")

    exp_time = datetime.utcnow() + timedelta(minutes=settings.EXP_TIME)

    token = jwt.encode(
        {"id": user.id, "exp": exp_time},
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )

    return {"token": token}


def isauthenticated(request: Request):

    token = request.headers.get("Authorization")

    if not token:
        raise HTTPException(status_code=401, detail="Token missing")

    token = token.split(" ")[-1]

    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )

        user_id = payload.get("id")

        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")

        return {
            "id": user_id   
        }

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")

    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
