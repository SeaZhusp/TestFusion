from datetime import datetime, timedelta, timezone
import jwt

from app.config import settings


class LoginManage:

    @staticmethod
    def create_token(data: dict, expires_delta: timedelta = None):
        expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=settings.jwt_token_expire_minutes))
        data.update({"exp": expire})
        return jwt.encode(data, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)
