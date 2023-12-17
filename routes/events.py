# routes/events.py

from fastapi import APIRouter, HTTPException, status, Body, Depends, Request
from database.connection import get_session
from models.events import Event, EventUpdate
from typing import List
from sqlmodel import select, delete

event_router = APIRouter(
    tags=["Events"]
)

events = []

@event_router.get("/", response_model=List[Event])
async def retrieve_all_events(session=Depends(get_session)) -> List[Event]:
    statement = select(Event)
    events = session.exec(statement).all()
    return events

@event_router.get("/{id}", response_model=Event)
async def retrieve_event(id: int, session=Depends(get_session)) -> Event:
    event = session.get(Event, id)
    if event:
        return event
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Event with supplied ID does not exist"
    )

# @event_router.post("/new")
# async def create_event(body: Event = Body(...)) -> dict:  
#     """
#     Body(...) 는 여러 개의 필드를 가진 클래스를 URL 요청으로 보내기 어렵기 때문에(경로 매개변수나 쿼리 매개변수로 인식)
#     Body(요청의 본문) 이라는 표시를 해주는 것. 이렇게 하지 않으면 오류 발생 가능
#     """
#     events.append(body)
#     return {
#         "message": "Event created successfully."
#     }

@event_router.post("/new")
async def create_event(new_event: Event, session=Depends(get_session)) -> dict:
    session.add(new_event)
    session.commit()
    session.refresh(new_event)

    return {
        "message": "Event created successfully."
    }

@event_router.put("/edit/{id}", response_model=Event)
async def update_event(id: int, new_data: EventUpdate, session=Depends(get_session)) -> Event:
    event = session.get(Event, id)
    if event:
        event_data = new_data.model_dump(exclude_unset=True)
        for key, value in event_data.items():
            setattr(event, key, value)
        session.add(event)
        session.commit()
        session.refresh(event)
        return event
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Event with supplied ID does not exist"
    )

@event_router.delete("/delete/{id}")
async def delete_event(id: int, session=Depends(get_session))-> dict:
    event = session.get(Event, id)
    if event:
        session.delete(event)
        session.commit()
        return {
            "message": "Event deleted successfully."
        }

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Event with supplied ID does not exist"
    )

@event_router.delete("/delete_all")
async def delete_all_events(session=Depends(get_session)) -> dict:
    statement = delete(Event)
    session.exec(statement)
    session.commit()

    return {
        "message": "Events deleted successfully."
    }