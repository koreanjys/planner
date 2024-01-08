# routes/users.py

from auth.hash_password import HashPassword
from database.connection import Database

from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
"""
OAuth2PasswordRequestForm 클래스는 인증 정보(사용자명과 패스워드)를
추출하기 위해 로그인 라우트에 주입될 것이다.
"""

from auth.jwt_handler import create_access_token

from models.users import User, TokenResponse

user_router = APIRouter(
    tags=["User"],  # 자동 API 문서화에서 User 태그로 그룹화
)

user_database = Database(User)
hash_password = HashPassword()

users = {}

@user_router.post("/signup")
async def sign_new_user(user: User) -> dict:
    user_exist = await User.find_one(User.email == user.email)
    """
    User.find_one() 은 User 컬렉션에서 하나의 문서를 찾는다.
    (User.email==user.email)은 User 컬렉션의 email필드가 user.email 과 같은게 있는지 확인하는 구문이다.
    beanie의 직관성이 돋보이는 구문이다.
    """
    if user_exist:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with email provided exists already"
        )
    hashed_password = hash_password.create_hash(user.password)  # 암호를 해싱
    user.password = hashed_password  # 해싱한 암호를 user 정보에 입력
    await user_database.save(user)  # DB에 user 정보를 저장(해싱된 암호로 저장)
    return {
        "message": "User successfully registered!"
    }

@user_router.post("/signin", response_model=TokenResponse)
async def sign_user_in(user: OAuth2PasswordRequestForm = Depends()) -> dict:
    """
    (user: OAuth2PasswordRequestForm = Depends()) 이 부분 해석:
    "OAuth2PasswordRequestForm"의 인스턴스를 생성하여 "user" 인자에 할당한다는 뜻.
    그리고 "= Depends()"를 사용함으로써 FastAPI에게 "sign_user_in"가 "OAuth2PasswordRequestForm"의 인스턴스가
    필요로 한다는 것을 알려준다. 그리고 FastAPI는 인스턴스에 담길 정보들을 OAuth2 사양을 엄격하게 따르도록 하고,
    정보가 담긴 인스턴스를 user 인자에 할당하는 과정을 알아서 처리해준다.

    그러면 왜 (user: OAuth2PasswordRequestForm) 이렇게 인자를 받지 않고, 꼭 "= Depends()"를 사용해야 하는가?:
    FastAPI에서 `user: OAuth2PasswordRequestForm`처럼 사용하면,
    FastAPI는 이를 자동으로 인스턴스화하려고 시도할 것입니다.
    그러나 `OAuth2PasswordRequestForm`은 FastAPI 경로 작업에서 직접 인스턴스화할 수 없는 특별한 클래스입니다.
    `OAuth2PasswordRequestForm`은 사용자로부터 username과 password를
    안전하게 수집하기 위한 폼 데이터를 정의하는 클래스입니다.
    이 클래스의 인스턴스는 FastAPI가 HTTP 요청을 처리하고 폼 데이터를 파싱한 후에 만들어집니다.
    이런 과정은 FastAPI의 내부 동작 방식에 따라 이루어지는 것입니다.
    따라서 `Depends()`를 사용하여 `OAuth2PasswordRequestForm`을 의존성으로 선언해야 합니다.
    이렇게 하면 FastAPI는 `sign_user_in` 함수를 호출하기 전에 필요한 작업(즉, HTTP 요청 처리와 폼 데이터 파싱)을
    수행하고, 그 결과인 `OAuth2PasswordRequestForm` 인스턴스를 함수에 주입할 수 있습니다.
    간단히 말하면, `Depends()`를 사용하는 이유는 FastAPI에게
    `sign_user_in` 함수가 `OAuth2PasswordRequestForm` 인스턴스를 필요로 한다는 것을 알려주고,
    이를 생성하고 주입하는 과정을 FastAPI에게 맡기기 위함입니다.
    *즉, `OAuth2PasswordRequestForm`는 '= Depends()'를 꼭 사용해줘야 하는 특별한 클래스다.
    "= Depends()"를 해줘야 FastAPI가 알아서 OAuth2PasswordRequestForm에 안전하게 유저 정보를 받아서
    user 인자에 "유저 정보가 담긴 인스턴스"를 주입해주는 것이다.
    """
    user_exist = await User.find_one(User.email == user.username)  # DB에서 user.username과 같은 이메일의 데이터를 찾음
    if not user_exist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User does not exist"
        )
    
    # if user_exist.password != user.password:  # 해싱되지 않아 안전하지 않은 암호 검증 방법
    #     raise HTTPException(
    #         status_code=status.HTTP_403_FORBIDDEN,
    #         detail="Wrong credentials passed"
    #     )

    if hash_password.verify_hash(user.password, user_exist.password):
        # user로부터 받은 원본 암호와 DB에 저장되어있는 해싱된 암호를 비교하고 인증한다.
        
        access_token = create_access_token(user_exist.email)
        # 사용자 정보와 암호가 전부 검증이 되었다면, "access_token", "token_type"이 담긴 dict를 반환한다.
        return {
            "access_token": access_token,
            "token_type": "Bearer"
        }
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid details passed"
    )