import os


class JwtSettings:
    def __init__(self):
        self.SECRET_KEY = os.getenv("SECRET_KEY", "supersecret")
        self.ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
        self.ACCESS_TOKEN_EXPIRE_MINUTES: int = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30)


jwt_settings = JwtSettings()
