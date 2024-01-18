# PLANNER

## 1. App architecture

PLANNER
- main.py : PLANNER 앱의 진입점. 앱의 시작 및 시작 설정 등을 정의한다.
- auth : 사용자 인증 및 권한 부여를 담당한다.
- database : DB와 연결을 관리하고, CRUD를 담당한다.
- routes : 라우트를 정의하고, 각 URL경로에 대해 어떤 동작을 수행할지 정의한다.
- store : MongoDB의 데이터를 저장하고 관리하는 폴더.
- models : DB의 테이블 구조와 데이터 모델의 형태를 정의한다.

### 1.1 auth
- authenticate.py : 토큰을 추출하여 검증하고 디코딩해서 유저 정보를 반환해주는 함수가 들어있다.
- hashpassword.py : 암호를 해싱하는 함수, 기존 암호와 해싱된 암호가 일치하는지 확인하는 함수가 들어있다.
- jwt_handler.py : JWT를 인코딩, 디코딩하는 함수가 들어있다.

### 1.2 database
- connection.py : 데이터베이스와의 연결을 초기화 해주는 함수, 데이터베이스의 CRUD를 구현하는 함수가 들어있다.

### 1.3 routes
- events.py : 이벤트 생성, 읽기, 수정, 지우기를 요청 및 응답을 하는 함수들이 정의되어 있다.
- users.py : 사용자 회원가입(암호 해싱), 로그인(해싱 암호 확인 및 토큰 발급) 요청 및 응답을 하는 함수가 정의되어 있다.

### 1.4 models
- events.py : 이벤트 생성 모델(MongDB의 events 컬렉션과 연결되는)과 이벤트 업데이트 모델이 정의되어 있다.
- users.py : 사용자 회원가입 모델(MongoDB의 users 컬렉션과 연결되는)과 토큰 모델이 정의되어 있다.

## beanie
- beanie==1.13.1  # beanie 1.13.1 버전에서 작성
- Beanie - is an asynchronous Python object-document mapper (ODM) for MongoDB. Data models are based on Pydantic.

## mongodb
- 7.0.4 ver(2023-12-28 기준)
- Platform: Windows x64
- Package: msi
- [다운로드 페이지](https://www.mongodb.com/try/download/community)
