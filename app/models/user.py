from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.models.base import Base

ph = PasswordHasher()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, nullable=False, unique=True)
    login = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)

    def hash_password(self, password):
        self.password = ph.hash(password)

    def check_password(self, password):
        try:
            return ph.verify(self.password, password)
        except VerifyMismatchError:
            return False
