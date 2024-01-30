# tests/test_login.py
"""
경고문구와 에러1개 발생
에러는 이벤트 루프가 닫혔다는 에러인데 왜 발생하는지 원인 파악 필요..
"""

import httpx
import pytest

@pytest.mark.asyncio
async def test_sign_new_user(default_client: httpx.AsyncClient) -> None:
    payload = {
        "email": "testuser3@packt.com",
        "password": "testpassword",
        "username": "packt3"
    }
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json"
    }
    test_response = {
        "message": "User successfully registered!"
    }
    response = await default_client.post("/user/signup", json=payload, headers=headers)

    assert response.status_code == 200
    assert response.json() == test_response