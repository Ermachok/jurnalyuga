from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from fastapi.templating import Jinja2Templates
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.config.settings import jwt_settings
from app.database import get_db_session
from app.models.user import User

templates = Jinja2Templates(directory="app/templates")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/users/login")


async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db_session)):
    credentials_exception = HTTPException(status_code=401, detail="Не авторизован",
                                          headers={"WWW-Authenticate": "Bearer"})

    try:
        payload = jwt.decode(token, jwt_settings.SECRET_KEY, algorithms=[jwt_settings.ALGORITHM])
        login: str = payload.get("sub")
        if login is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = await db.execute(select(User).where(User.login == login))
    user = user.scalar_one_or_none()
    if user is None:
        raise credentials_exception

    return user
