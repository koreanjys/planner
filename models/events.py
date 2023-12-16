# models/events.py

from sqlmodel import JSON, SQLModel, Field, Column
from typing import List, Optional

class Event(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    title: str
    image: str
    description: str
    tags: List[str] = Field(sa_column=Column(JSON))
    location: str

    model_config = {
        # "arbitrary_types_allowed": True,  # 임의의 타입들을 허용한다는 코드
        "json_schema_extra": {
            "example": {
                # "id": 1,  # Field()에서 인자로 default=None을 해서 필요없음
                "title": "FastAPI Book Launch",
                "image": "https://linktomyimage.com/image.png",
                "description": "We will be discussing the contents of the FastAPI\
                      book in this event. Ensure to come with your own copy to win gifts",
                "tags": ["python", "fastapi", "book", "launch"],
                "location": "Google Meet"
            }
        }
    }

class EventUpdate(SQLModel):
    title: Optional[str]  
    image: Optional[str]
    description: Optional[str]
    tags: Optional[List[str]]
    location: Optional[str]

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "FastAPI Book Launch",
                "image": "https://linktomyimage.com/image.png",
                "description": "We will be discussing the contents of the FastAPI book ...",
                "tags": ["python", "fastapi", "book"],
                "location": "Google Meet",
            }
        }
    }