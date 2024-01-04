# auth/hash_password.py

# 패스워드를 암호화하는 함수가 포함된다. 이 함수는 계정을 등록할 때 또는 로그인 시 패스워드를 비교할 때 사용된다.

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class HashPassword:
    def create_hash(self, password: str):  # 일반 텍스트 패스워드를 암호화(해싱)하는 함수
        return pwd_context.hash(password)
    
    def verify_hash(self, plain_password: str, hashed_password: str):
        """
        일반 텍스트 패스워드와 해싱한 패스워드를 인수로 받아 두 값이 일치하는지 비교한다.
        일치 여부에 따라 boolean값을 반환한다.
        """
        return pwd_context.verify(plain_password, hashed_password)