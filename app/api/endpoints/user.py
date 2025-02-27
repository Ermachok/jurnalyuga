from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.database import get_db_session
from app.models.user import User
from app.schemas.user import UserRegistration, UserRegistrationResponse

router = APIRouter(prefix="/api/users", tags=["Users"])


@router.post("/register", response_model=UserRegistrationResponse, status_code=status.HTTP_201_CREATED)
async def registrate_user(user_data: UserRegistration, db: AsyncSession = Depends(get_db_session)):
    print(user_data)
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
