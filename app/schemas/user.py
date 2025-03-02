from pydantic import BaseModel


class UserRegistration(BaseModel):
    email: str
    login: str
    password: str | int


class UserLogin(BaseModel):
    email_or_login: str
    password : str


class UserLoginResponse(BaseModel):
    result: bool


class UserRegistrationResponse(BaseModel):
    result: bool

