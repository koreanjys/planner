# routes/events.py

from beanie import PydanticObjectId
from fastapi import APIRouter, HTTPException, status, Depends
from database.connection import Database

from models.events import Event, EventUpdate
from auth.authenticate import authenticate

from typing import List

event_router = APIRouter(
    tags=["Events"]
)

event_database = Database(Event)

# events = []  # DB서버 구축하면서 필요없어짐

@event_router.get("/", response_model=List[Event])
async def retrieve_all_events() -> List[Event]:
    events = await event_database.get_all()
    return events

@event_router.get("/{id}", response_model=Event)
async def retrieve_event(id: PydanticObjectId) -> Event:
    event = await event_database.get(id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event with supplied ID does not exist"
        )
    return event

# @event_router.post("/new")  # 임시 post
# async def create_event(body: Event = Body(...)) -> dict:  
#     """
#     Body(...) 는 여러 개의 필드를 가진 클래스를 URL 요청으로 보내기 어렵기 때문에(경로 매개변수나 쿼리 매개변수로 인식)
#     Body(요청의 본문) 이라는 표시를 해주는 것. 이렇게 하지 않으면 오류 발생 가능. 보통 dict? json? 키밸류 형태
#     """
#     events.append(body)
#     return {
#         "message": "Event created successfully."
#     }

@event_router.post("/new")
async def create_event(body: Event, user: str = Depends(authenticate)) -> dict:
    # Depends(authenticate)로 인해 토큰으로 인증된 유저만 이벤트 CUD가 가능해졌다.

    body.creator = user  # 신규 이벤트를 만들면 해당 이벤트에 생성자의 이메일이 함께 저장된다.

    await event_database.save(body)  # Event 모델의 인스턴스인 body는 Settings에 입력한 "events" 컬렉션에 저장된다.
    """
    create_event 함수에 쿼리가 따로 없는 이유:
    Event 모델에 Settings 클래스에서 Event 모델 형태로 저장될 컬렉션 위치를 입력해놨기 때문에 바로 저장이 된다.
    즉, Event 모델 형태로 만들어진 body(doc)는 무조건 DB의 events 컬렉션에 저장된다.
    """
    return {
        "message": "Event created successfully."
    }

@event_router.put("/{id}", response_model=Event)
async def update_event(id: PydanticObjectId, body: EventUpdate, user: str = Depends(authenticate)) -> Event:
    update_event = await event_database.update(id, body)
    if not update_event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event with supplied ID does not exist"
        )
    return update_event
    

@event_router.delete("/{id}")
async def delete_event(id: PydanticObjectId, user: str = Depends(authenticate))-> dict:
    event = await event_database.delete(id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event with supplied ID does not exist"
        )
    return {
        "message": "Event deleted successfully."
    }

# @event_router.delete("/")
# async def delete_all_events() -> dict:
#     events.clear()
#     return {
#         "message": "Events deleted successfully."
#     }