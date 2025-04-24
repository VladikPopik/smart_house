import typing as ty
from datetime import datetime, timedelta

import jwt
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext

import httpx

from lib.conf import config
from lib.db.mysql.user import crud as u_crud
from lib.manager.auth.schemas import CreateUser, GetToken, LoginUser, UserLogin
from logging import getLogger


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

auth_router = APIRouter()

auth_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

SECRET_KEY = config.JWT.SECRET_KEY
ALGORITHM = config.JWT.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = config.JWT.ACCESS_TOKEN_EXPIRE_MINUTES

logger = getLogger()

def create_access_token(
    data: ty.Dict[str, ty.Any], expires_delta: timedelta | None = None
):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str = Depends(auth_scheme)):
    try:
        payload: str = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str | None = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=403, detail="Token is invalid or expired"
            )
        return payload
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=403, detail="Token is invalid or expired"
        )


@auth_router.post("/register/")
async def register(user: CreateUser) -> dict[str, ty.Any]:
    db_user = await u_crud.get_user(user.user_login)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username {user.name} already registered",
        )
    hashed_password = pwd_context.hash(user.password)
    user.password = hashed_password
    await u_crud.create_user(user.model_dump(exclude="password"))
    await u_crud.register_user(
        {"user_login": user.user_login, "user_password": user.password}
    )
    return {"message": "User sucessfully created", "username": user.user_login}


@auth_router.post("/token", response_model=GetToken)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    user = LoginUser(user_login=form_data.username, password=form_data.password)
    db_user = await u_crud.get_user(user.user_login)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.user_login}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@auth_router.get("/verify-token/{token}")
async def verify_user_token(token: str) -> dict[str, str]:
    """Function to verify token."""
    verify_token(token=token)
    return {"message": "Token is valid"}


@auth_router.get("/logout")
async def logout() -> ty.Literal[True]:
    """Logout."""
    return True


@auth_router.post("/face/register")
async def face_register(user_login: UserLogin) -> dict[str, ty.Any]:
    try:
        # TODO<VladikPopik>: Create request from face recognition and get response
        # async with httpx.AsyncClient(timeout=5000) as client:
        #     response = await client.get(
        #         "http://backend:8001/settings/devices"
        #     )
        # access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        # access_token = create_access_token(
        #     data={"sub": user_login}, expires_delta=access_token_expires
        # )
        return {"success": True, "login": user_login}
    except Exception as e:
        logger.exception(e)

@auth_router.post("/token/face_recognition", response_model=GetToken)
async def login_facerecognition() -> dict[str, ty.Any]:
    #TODO<VladikPopik>: Create request from face recognition and get response
    try:
        #async with httpx.AsyncClient(timeout=5000) as client:
        #     response = await client.get(
        #         "http://backend:8001/settings/devices"
        #     )
        response = {"login": "Vlad"}
    except Exception:
        return JSONResponse(content="Невозможно получить токен, попробуйте позже", status_code=400)


    try:
        user_login = response.get("login", None)
        if not user_login:
            raise ValueError

        db_user = await u_crud.get_user(user_login=user_login)
        if not db_user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user_login}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}
    except Exception as e:
        logger.exception(e)
        return JSONResponse(content="Невозможно получить токен, попробуйте позже", status_code=400)