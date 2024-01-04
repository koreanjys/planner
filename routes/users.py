# routes/users.py

from auth.hash_password import HashPassword
from database.connection import Database

from fastapi import APIRouter, HTTPException, status

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
    hashed_password = hash_password.create_hash(user.password)
    user.password = hashed_password
    await user_database.save(user)
    return {
        "message": "User successfully registered!"
    }

@user_router.post("/signin")
async def sign_user_in(user:UserSignIn) -> dict:  # 간단한 유저 인증. 권장 X
    user_exist = await User.find_one(User.email == user.email)  # DB에서 user.email과 같은 이메일의 데이터를 불러옴
    if not user_exist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User does not exist"
        )
    if user_exist.password != user.password:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Wrong credentials passed"
        )
    
    return {
        "message": "User signed in successfully."
    }