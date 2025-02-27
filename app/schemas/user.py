from pydantic import BaseModel


class UserRegistration(BaseModel):
    email: str
    login: str
    password: str | int

class UserRegistrationResponse(BaseModel):
    result: bool
