# tests/test_arithmetic_operations.py
"""
일반적으로 테스트 파일이 아닌 별도의 파일에 테스트 대상 함수 (add(), substrat(), multiply(), divide())를
정의한다. 그런 다음 이 파일을 테스트 파일에 import하여 테스트를 수행한다.

테스트 방법은 $ pytest test_arithmetic_operations.py 를 실행한다.
"""

# 사칙연산 함수

def add(a: int, b: int) -> int:
    return a + b


def subtract(a: int, b: int) -> int:
    return b - a


def multiply(a: int, b: int) -> int:
    return a * b


def divide(a: int, b: int) -> int:
    return b // a


################################################################################
# 사칙연산 테스트
def test_add() -> None:
    assert add(1, 1) == 11


def test_subtract() -> None:
    assert subtract(2, 5) == 3


def test_multiply() -> None:
    assert multiply(10, 10) == 100


def test_divide() -> None:
    assert divide(25, 100) == 4


# 픽스처를 사용한 반복 제거
import pytest
from models.events import EventUpdate

# 픽스처 정의
@pytest.fixture
def event() -> EventUpdate:
    return EventUpdate(
        title="FastAPI Book Launch",
        image="이미지?",
        description="주석?",
        tags=["태그?"],
        location="위치?"
    )


def test_event_name(event: EventUpdate) -> None:
    assert event.title == "FastAPI Book Launch"