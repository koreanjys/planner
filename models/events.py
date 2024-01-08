# models/events.py

from typing import List, Optional
from beanie import Document
from pydantic import BaseModel

class Event(Document):
    """
    Document를 인자로 받은 Event 모델은 자동으로 _id를 생성
    이 _id는 PydanticObjectID 형태로, 해당 모델의 컬렉션과 상호작용이 가능해진다.
    """
    title: str
    image: str
    description: str
    tags: List[str]
    location: str

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "FastAPI Book Launch",
                "image": "https://linktomyimage.com/image.png",
                "description": "We will be discussing the contents of the FastAPI\
                      book in this event. Ensure to come with your own copy to win gifts",
                "tags": ["python", "fastapi", "book", "launch"],
                "location": "Google Meet"
            }
        }
    }

    class Settings:
        name = "events"  # 저장할 콜렉션 이름


class EventUpdate(BaseModel):  
    """
    EventUpdate 인자로 Document가 아닌 BaseModel을 받은 이유는 다음과 같다.
    
    1. 이 클래스는 HTTP 요청을 통해 클라이언트로부터 받은 데이터를 검증하고
      처리하는 데 사용되는 Pydantic 모델입니다.
      이 클래스는 데이터의 유효성을 검사하거나 기본 값을 설정하는 등의 작업을 수행하지만,
      MongoDB와 직접적으로 상호작용하는 기능은 필요하지 않습니다. 따라서 Document를 상속받지 않아도 됩니다.

    2. 이렇게 분리하여 구현하는 이유는 관심사의 분리 (Separation of Concerns) 원칙에 따른 것입니다.
      즉, 각 클래스는 자신의 역할에 집중하고, 그 외의 기능은 다른 클래스에서 처리하도록 합니다.
      이는 코드의 유지보수성과 확장성을 향상시키는 데 도움을 줍니다.
    """
    title: Optional[str] = None
    image: Optional[str] = None
    description: Optional[str] = None
    tags: Optional[List[str]] = None
    location: Optional[str] = None

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "FastAPI Book Launch",
                "image": "https://linktomyimage.com/image.png",
                "description": "We will be discussing the contents of the FastAPI\
                      book in this event. Ensure to come with your own copy to win gifts",
                "tags": ["python", "fastapi", "book", "launch"],
                "location": "Google Meet"
            }
        }
    }