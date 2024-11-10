from lib.utils.basemodel import Base


class CreateUser(Base):
    user_name: str = "Default"
    user_login: str
    user_email: str
    tg_login: str
    password: str
    is_superuser: bool = False


class RegisterUser(Base):
    user_login: str
    password: str


class GetToken(Base):
    access_token: str
    token_type: str = "bearer"


class LoginUser(Base):
    user_login: str
    password: str
