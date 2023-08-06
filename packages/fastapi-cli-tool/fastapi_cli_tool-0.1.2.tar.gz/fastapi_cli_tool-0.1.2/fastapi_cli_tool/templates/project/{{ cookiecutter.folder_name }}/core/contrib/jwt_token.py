from datetime import datetime, timedelta
from typing import Optional

from backend.settings import settings
from fastapi import HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from pydantic import BaseModel, EmailStr


class TokenData(BaseModel):
    email: EmailStr


class JWTToken(HTTPBearer):
    def __init__(self, auto_error: bool = False):
        super(JWTToken, self).__init__(auto_error=auto_error)
        pass

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(
            JWTToken, self
        ).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid authentication scheme.",
                )
            if not self.verify_token(
                credentials.credentials, "Could not validate credentials"
            ):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid token or expired token.",
                )
            return credentials.credentials
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authorization code.",
            )

    def create_access_token(
        self, data: dict, expires_delta: Optional[timedelta] = None
    ):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + settings.JWT["ACCESS_TOKEN_LIFETIME"]
        to_encode.update({"exp": expire, "iat": datetime.utcnow()})
        encode_jwt = jwt.encode(
            to_encode,
            settings.JWT["JWT_SECRET_KEY"],
            algorithm=settings.JWT["ALGORITHM"],
        )
        return encode_jwt

    def create_refresh_token(
        self, data: dict, expires_delta: Optional[timedelta] = None
    ):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + settings.JWT["REFRESH_TOKEN_LIFETIME"]
        to_encode.update({"exp": expire, "iat": datetime.utcnow()})
        encode_jwt = jwt.encode(
            to_encode,
            settings.JWT["JWT_REFRESH_SECRET_KEY"],
            algorithm=settings.JWT["ALGORITHM"],
        )
        return encode_jwt

    def verify_token(
        self,
        token: str,
        credentials_exception,
        key: str = settings.JWT["JWT_SECRET_KEY"],
    ):
        try:
            payload = jwt.decode(
                token=token, key=key, algorithms=settings.JWT["ALGORITHM"]
            )
            email: str = payload.get("sub")
            if email is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail=credentials_exception,
                )
            token_data = TokenData(email=email)
            return token_data
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail=credentials_exception
            )
