from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from src.utils.db import get_db
from src.users import controller
from src.users.dtos import UserSchema, LoginSchema, UserResponseSchema

user_routes = APIRouter(prefix="/users")


@user_routes.post("/create", response_model=UserResponseSchema)
def create_user(body: UserSchema, db: Session = Depends(get_db)):
    return controller.create_user(body, db)



@user_routes.post("/login")
def login_user(body: LoginSchema, db: Session = Depends(get_db)):
    return controller.login_user(body, db)



@user_routes.get("/is_auth")
def is_auth(request: Request):
    return controller.isauthenticated(request)
 