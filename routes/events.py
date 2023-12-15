# routes/events.py

from fastapi import APIRouter, HTTPException, status, Body
from models.events import Event
from typing import List

event_router = APIRouter(
    tags=["Events"]
)

events = []

@event_router.get("/", response_model=List[Event])
async def retrieve_all_events() -> List[Event]:
    return events

@event_router.get("/{id}", response_model=Event)
async def retrieve_event(id: int) -> Event:
    for event in events:
        if event.id == id:
            return event
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Event with supplied ID does not exist"
    )

@event_router.post("/new")
async def create_event(body: Event = Body(...)) -> dict:  
    """
    Body(...) 는 여러 개의 필드를 가진 클래스를 URL 요청으로 보내기 어렵기 때문에(경로 매개변수나 쿼리 매개변수로 인식)
    Body(요청의 본문) 이라는 표시를 해주는 것. 이렇게 하지 않으면 오류 발생 가능
    """
    events.append(body)
    return {
        "message": "Event created successfully."
    }

@event_router.delete("/{id}")
async def delete_event(id: int)-> dict:
    for event in events:
        if event.id == id:
            events.remove(event)
            return {
                "message": "Event deleted successfully."
            }
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Event with supplied ID does not exist"
    )

@event_router.delete("/")
async def delete_all_events() -> dict:
    events.clear()
    return {
        "message": "Events deleted successfully."
    }