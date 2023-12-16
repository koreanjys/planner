# main.py

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from typing import List
from database.connection import conn

from routes.users import user_router
from routes.events import event_router

import uvicorn
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    
    # yield 이전 코드 -> 앱 실행 시 작동되는 코드
    conn()
    
    yield
    # yield 이후 코드 -> 앱 종료 시 작동되는 코드 

app = FastAPI(lifespan=lifespan)

# 라우트 등록
app.include_router(user_router, prefix="/user")
app.include_router(event_router, prefix="/event")

# 앱 시작 시 실행하는 함수(이제 사용안함, 위에 lifespan 함수 사용)
# @app.on_event("startup")
# def on_startup():
#     conn()


# uvicorn 앱 실행
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)