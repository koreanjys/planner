# main.py

from fastapi import FastAPI
from database.connection import Settings
from contextlib import asynccontextmanager

from routes.users import user_router
from routes.events import event_router

import uvicorn

@asynccontextmanager
async def lifespan(app: FastAPI):
    await settings.initialize_database()  # 앱 시작시 db 초기화
    yield

app = FastAPI(lifespan=lifespan)
settings = Settings()

# 라우트 등록
app.include_router(user_router, prefix="/user")
app.include_router(event_router, prefix="/event")

# uvicorn 앱 실행
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)