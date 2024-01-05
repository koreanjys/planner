# auth/jwt_handler.py

# 주어진 사용자명을 JWT로 인코딩, 디코딩하는 함수가 포함된다.

import time
from datetime import datetime

from fastapi import HTTPException, status
from jose import jwt, JWTError
"""
jose는 JWT의 인코딩과 디코딩하는 라이브러리

설치방법은 아래 코드
$ pip install python-jose[cryptography] python-multipart
"""

from database.connection import Settings

settings = Settings()

def create_access_token(user: str):  # 토큰 생성 함수
    payload = {
        "user": user,
        "expires": time.time() + 3600  # 만료기간 +3600초(1시간)
    }

    token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
    return token