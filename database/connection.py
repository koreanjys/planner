from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from typing import Optional
from pydantic_settings import BaseSettings

from models.users import User
from models.events import Event

class Settings(BaseSettings):
    DATABASE_URL: Optional[str] = None

    async def initialize_database(self):
        client = AsyncIOMotorClient(self.DATABASE_URL)
        await init_beanie(database=client.get_default_database(), 
                          document_models=[User, Event]) 
        
    model_config ={
        "env_file": ".env"  # DATABASE_URL을 .env 파일에서 불러옴
    }