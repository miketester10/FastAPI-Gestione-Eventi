import time

import jwt
from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from src.config import settings as s


def sign_jwt(user_id: int) -> dict[str, str]:
    # Access Token
    at_expiration_time = int(time.time()) + s.jwt_expires_in * 60
    at_payload = {"user_id": user_id, "type": "access", "exp": at_expiration_time}
    access_token = jwt.encode(
        at_payload, s.jwt_secret.get_secret_value(), algorithm=s.algorithm
    )
    # Refresh Token
    rt_expiration_time = int(time.time()) + s.jwt_refresh_expires_in * 60
    rt_payload = {"user_id": user_id, "type": "refresh","exp": rt_expiration_time}
    refresh_token = jwt.encode(
        rt_payload, s.jwt_refresh_secret.get_secret_value(), algorithm=s.algorithm
    )
    return {"access_token": access_token, "refresh_token": refresh_token}


def decode_jwt(token: str, is_refresh_token: bool) -> dict:
    secret = s.jwt_secret.get_secret_value()
    if is_refresh_token:
        secret = s.jwt_refresh_secret.get_secret_value()

    try:
        return jwt.decode(token, secret, algorithms=[s.algorithm])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Expired token.")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token.")


class JWTBearer(HTTPBearer):
    def __init__(self, is_refresh_token: bool = False, auto_error: bool = True):
        super().__init__(auto_error=auto_error)
        self.is_refresh_token = is_refresh_token

    async def __call__(self, request: Request) -> int:
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)
        if not credentials or not credentials.scheme == "Bearer":
            raise HTTPException(status_code=401, detail="Invalid authentication.")
        decoded_token = decode_jwt(credentials.credentials, self.is_refresh_token)

        return decoded_token.get("user_id")
