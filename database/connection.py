# database/connection.py

from sqlmodel import SQLModel, Session, create_engine
from models.events import Event

database_file = "planner.db"
database_connection_string = f"sqlite:///{database_file}"
connect_args = {"check_same_thread": False}
engine_url = create_engine(database_connection_string, echo=True, connect_args=connect_args)

def conn():
    SQLModel.metadata.create_all(engine_url)

def get_session():
    with Session(engine_url) as session:
        yield session
        """
        $ def func(data, session=Depends(get_session))
        위와 같이 어떤 함수에 의존성 주입으로 get_session 함수를 주입할 때
        yield 문으로 session을 반환하면 어떤 함수가 시작될 때 세션을 열고
        어떤 함수가 끝나면 세션이 닫히게 된다.

        DB 세션 yield 반환과 with문(콘텍스트 매니저), 그리고 Depends(의존성 주입)은
        하나의 세트로 사용되면 각 세션마다 새로운(독립적인) 세션이 되며
        세션이 열리고 닫히는것을 안정적으로 관리하는 기술이다. 라고 현재로써는 이정도만 이해하자..
        """
