import asyncio

from sqlalchemy import select

from app.database import async_session_maker
from app.models.user import User


async def create_test_data():
    async with async_session_maker() as session:
        result = await session.execute(select(User).limit(1))
        existing_user = result.scalars().first()

        if existing_user:
            return

        user0 = User(login="test", email='test@mail.ru', password ='test_pas')

        session.add_all([user0, ])
        await session.commit()

        await session.commit()


if __name__ == "__main__":
    asyncio.run(create_test_data())
