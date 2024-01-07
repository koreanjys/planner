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

def verify_access_token(token: str):  # 토큰 검증 함수
    try:
        data = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        """
        토큰을 디코딩해서 payload를 data변수로 받는다.
        """
        expire = data.get("expires")  # 딕셔너리의 get(x) 함수는 x라는 key에 대응되는 value값을 돌려준다.

        if expire is None:  # 만료 시간이 없다면 유효한 토큰이 존재하지 않음
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No access token supplied"
            )
        if datetime.utcnow() > datetime.utcfromtimestamp(expire):  # 토큰이 유효한지(만료 시간이 지나지 않았는지)
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Token expired!"
            )
        return data
    
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid token"
        )