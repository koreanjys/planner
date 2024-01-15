# auth/authenticate.py

# authenticate 의존 라이브러리가 포함되며 인증 및 권한을 위해 라우트에 주입된다.
# 이 함수는 활성 세션에 존재하는 사용자 정보를 추출하는 단일 창구 역할을 한다.

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from auth.jwt_handler import verify_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/signin")
"""
OAuth2PasswordBearer(tokenUrl) 클래스의 인스턴스 oauth2_scheme 변수는
보안 로직이 존재한다는 것을 애플리케이션에 알려준다.
token 문자열을 추출한다.
tokenUrl은 token을 받는 로그인 url을 입력한다.
"""

async def authenticate(token: str = Depends(oauth2_scheme)) -> str:
    """
    authenticate() 함수는 토큰을 인수로 받는다. 토큰이 유효하면 토큰을 디코딩한 후 페이로드의 사용자 필드를
    반환하고 유효하지 않으면 verify_access_token() 함수에 정의된 오류 메시지를 반환한다.
    라우트에 보안 적용을 위한 의존 라이브러리를 만들었다.
    """
    if not token:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Sign in for access"
        )

    decoded_token = verify_access_token(token)  # 토큰을 디코딩한다. "user"와 "expires"를 담고있다
    return decoded_token["user"]  # "user"만 반환한다.