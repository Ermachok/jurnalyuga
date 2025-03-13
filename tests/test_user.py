import pytest
from httpx import AsyncClient
from sqlalchemy import select

from app.models.user import User


@pytest.mark.anyio
async def test_user_registration(test_session, client: AsyncClient):
    """Тест регистрации нового пользователя"""
    user_data = {
        "email": "test@example.com",
        "login": "testuser",
        "password": "SecurePass123",
    }
    response = await client.post("/api/users/register", json=user_data)
    assert response.status_code == 201
    data = response.json()
    assert data["result"] is True

    # Проверяем, что пользователь добавился в БД
    user = await test_session.execute(
        select(User).where(User.email == user_data["email"])
    )
    assert user.scalar_one_or_none() is not None


@pytest.mark.anyio
async def test_user_login(test_session, client: AsyncClient):
    """Тест авторизации пользователя"""
    user_data = {
        "email": "test@example.com",
        "login": "testuser",
        "password": "SecurePass123",
    }
    # Сначала регистрируем пользователя
    await client.post("/api/users/register", json=user_data)

    # Затем логинимся
    response = await client.post(
        "/api/users/login",
        json={"email_or_login": "testuser", "password": "SecurePass123"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

    # Проверяем ошибку при неверном пароле
    response = await client.post(
        "/api/users/login", json={"email_or_login": "testuser", "password": "WrongPass"}
    )
    assert response.status_code == 401
