# main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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

# 출처 등록(교차 출처 리소스 공유 CORS)는 등록된 사용자만(프론트엔드 서버) 백엔드 서버의 리소스를 사용할 수 있게 한다.
origins = ["*"]  # "*"은 모든 클라이언트의 요청을 허가한다.

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우트 등록
app.include_router(user_router, prefix="/user")
app.include_router(event_router, prefix="/event")

# uvicorn 앱 실행
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)