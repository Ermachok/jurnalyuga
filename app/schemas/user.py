from pydantic import BaseModel


class UserRegistration(BaseModel):
    email: str
    login: str
    password: str | int


class UserLogin(BaseModel):
    email_or_login: str
    password: str


class UserLoginResponse(BaseModel):
    access_token: str
    token_type: str


class UserRegistrationResponse(BaseModel):
    result: bool
