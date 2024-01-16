# database/connection.py

from beanie import init_beanie, PydanticObjectId
from motor.motor_asyncio import AsyncIOMotorClient

from typing import Optional, Any, List
from pydantic import BaseModel
from pydantic_settings import BaseSettings

from models.users import User
from models.events import Event

class Settings(BaseSettings):  # 데이터베이스 초기화 세팅
    SECRET_KEY: Optional[str] = None
    DATABASE_URL: Optional[str] = None

    async def initialize_database(self):
        client = AsyncIOMotorClient(self.DATABASE_URL)  # MongoDB와 연결하기 위한 DB_URL을 인자로 받는 클래스  
        await init_beanie(database=client.get_default_database(), 
                          document_models=[User, Event])  # DB의 컬렉션과 상호작용하기 위해 모델 클래스를 넣어줌
        
    model_config ={
        "env_file": ".env"  # DATABASE_URL, SECRET_KEY를 .env 파일에서 불러오게 설정, pydantic[dotenv] 설치 필요
    }

class Database:  # 데이터베이스 클래스를 사용해서 MongoDB의 CRUD를 구현
    """
    beanie의 CRUD는 상당히 직관적이다.
    models에서 정의한 모델 클래스(Document를 상속한)는 연결할 컬렉션 이름이 설정되어있다. 그래서 DB와 상호작용이
    바로 가능하다.
    *save 함수는 인자로 받은 document 자체가 모델 클래스의 인스턴스라서 DB와 상호작용이 가능하다.
    """
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
        docs = await self.model.find_all().to_list()  # .to_list() 사용하는 이유는 pydantic의 모델 인스턴스 형태를
                                                      # python의 리스트 형태로 변경해 편리하게 사용하기 위함
        return docs
    
    async def update(self, id: PydanticObjectId, body: BaseModel) -> Any:  # Update 처리
        doc_id = id
        des_body = body.model_dump()  # pydantic 형태의 모델 인스턴스의 필드와 값을 python의 dict 형태로 변경.
                                      # TODO: 사용하기 편하기 위해 전처리라고 알고있음. 정확한 이유는 아직 모름
        des_body = {k:v for k, v in des_body.items() if v is not None}  # 값이 None인 필드를 제거 처리
        update_query = {"$set": {field:value for field, value in des_body.items()}}
        """
        {"$set": 딕셔너리 값} : 업데이트 쿼리를 날리기 위해 $set을 키 값으로 사용
        TODO: 왜 update_query 변수에서 바로 des_body를 안쓰고 컴프리헨션을 쓰는지?
              이전 버전에서 에러 발생 or 메모리를 절약? ***아직 알수 없음***
        """

        doc = await self.get(doc_id)
        """
        doc 변수에 원본 DB데이터를 받음
        여기서 self.get의 get은 현재 Class의 get 함수다.
        그래서 위 get 함수에서는 beanie의 model.get(id)를 사용했지만,
        여기서는 get(id)만 사용하여 현재 Class의 get 함수를 불러온다.
        그렇게도 DB와 상호작용이 가능하다.
        """
        if not doc:
            return False
        await doc.update(update_query)  # 원본 doc 데이터 변수를 update_query 변수로 업데이트
        return doc
    
    async def delete(self, id: PydanticObjectId) -> bool:  # Delete 처리
        doc = await self.get(id)
        if not doc:
            return False
        await doc.delete()
        return True