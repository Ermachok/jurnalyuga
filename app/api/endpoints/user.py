from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from jose import jwt
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.database import get_db_session
from app.models.user import User
from app.schemas.user import (
    UserLogin,
    UserLoginResponse,
    UserRegistration,
    UserRegistrationResponse,
)

SECRET_KEY = "VERYSECRETKEY"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.now() + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


router = APIRouter(prefix="/api/users", tags=["Users"])


@router.post(
    "/register",
    response_model=UserRegistrationResponse,
    status_code=status.HTTP_201_CREATED,
)
async def registrate_user(
    user_data: UserRegistration, db: AsyncSession = Depends(get_db_session)
):
    existing_user = await db.execute(select(User).where(User.email == user_data.email))
    if existing_user.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь с таким email уже существует",
        )

    existing_user = await db.execute(select(User).where(User.login == user_data.login))
    if existing_user.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь с таким логином уже существует",
        )

    new_user = User(
        email=user_data.email,
        login=user_data.login,
    )
    new_user.hash_password(user_data.password)

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return UserRegistrationResponse(result=True)


@router.post("/login", response_model=UserLoginResponse, status_code=status.HTTP_200_OK)
async def login_user(user_data: UserLogin, db: AsyncSession = Depends(get_db_session)):
    user = await db.execute(
        select(User).where(
            (User.email == user_data.email_or_login)
            | (User.login == user_data.email_or_login)
        )
    )
    user = user.scalar_one_or_none()

    if not user or not user.check_password(user_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный email/логин или пароль",
        )

    access_token = create_access_token({"sub": user.login})
    return UserLoginResponse(access_token=access_token, token_type="bearer")
