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

from models.users import User, UserSignIn

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

@user_router.post("/signin")
async def sign_user_in(user: OAuth2PasswordRequestForm = Depends()) -> dict:
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
        """
        user로부터 받은 원본 암호와 DB에 저장되어있는 해싱된 암호를 비교하고 인증한다.
        """
        access_token = create_access_token(user_exist.email)
        return {
            "access_token": access_token,
            "token_type": "Bearer"
        }
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid details passed"
    )