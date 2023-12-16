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
        yield를 사용한 이유는, get_session() 함수를 with문과 함께 사용하기 위해서이다. with문은 
        컨텍스트 매니저의 __enter__ 메소드를 호출하여 리소스를 할당하고, __exit__ 메소드를 호출하여 
        리소스를 해제한다. get_session() 함수에서는 yield 이전의 부분에서 세션을 생성(__enter__에 해당)하고, 
        yield 이후의 부분에서 세션을 닫음(__exit__에 해당).
        
        예시)
        with get_session() as session:
            # 세션을 사용하는 코드
        """

    