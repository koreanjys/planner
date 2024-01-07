# models/users.py

from beanie import Document, Link
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from models.events import Event

class User(Document):
    email: EmailStr  # email 형식에 맞는지 검사
    password: str
    username: str
    events: Optional[List[Event]] = []  # Optioanl을 사용할 때 None 값이라도 미리 정해주지 않으면 에러가 발생한다. 그러니 = None 이라도 값을 주자

    model_config = {
        "json_schema_extra": {
            "example": {
                "email": "fastapi@packt.com",
                "password": "strong!!!",
                "username": "FastPackt"
            }
        }
    }

    class Settings:
        name = "users"

# class UserSignIn(BaseModel):  # 안전하지 않은 로그인 모델
#     email: EmailStr
#     password: str

#     model_config = {
#         "json_schema_extra": {
#             "example": {
#                 "email": "fastapi@packt.com",
#                 "password": "strong!!!",
#             }
#         }
#     }

