# database/connection.py

from beanie import init_beanie, PydanticObjectId
from motor.motor_asyncio import AsyncIOMotorClient

from typing import Optional, Any, List
from pydantic import BaseModel
from pydantic_settings import BaseSettings

from models.users import User
from models.events import Event

class Settings(BaseSettings):  # 데이터베이스 초기화 세팅
    DATABASE_URL: Optional[str] = None

    async def initialize_database(self):
        client = AsyncIOMotorClient(self.DATABASE_URL)
        await init_beanie(database=client.get_default_database(), 
                          document_models=[User, Event]) 
        
    model_config ={
        "env_file": ".env"  # DATABASE_URL을 .env 파일에서 불러옴
    }

class Database:  # 데이터베이스 클래스를 사용해서 MongoDB의 CRUD를 구현
    def __init__(self, model):
        self.model = model

    async def save(self, document) -> None:  # Create 처리
        await document.create()
        return
    
    async def get(self, id: PydanticObjectId) -> Any:  # Read 처리(단일 레코드)
        doc = await self.model.get(id)
        if doc:
            return doc
        return False
    
    async def get_all(self) -> List[Any]:  # Read 처리(전체 레코드)
        docs = await self.model.find_all().to_list()
        return docs
    
    async def update(self, id: PydanticObjectId, body: BaseModel) -> Any:  # Update 처리
        doc_id = id
        des_body = body.model_dump()
        des_body = {k:v for k, v in des_body.items() if v is not None}
        update_query = {"$set": {field:value for field, value in des_body.items()}}

        doc = await self.get(doc_id)
        if not doc:
            return False
        await doc.update(update_query)
        return doc
    
    async def delete(self, id: PydanticObjectId) -> bool:  # Delete 처리
        doc = await self.get(id)
        if not doc:
            return False
        await doc.delete()
        return True