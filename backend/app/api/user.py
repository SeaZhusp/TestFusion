from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies.database import db_getter
from app.core.response import SuccessResponse
from app.schemas.user import LoginIn
from app.services.user import UserService

router = APIRouter(prefix="/user")


@router.post("/login")
async def login(
        login_in: LoginIn,
        db: AsyncSession = Depends(db_getter)
):
    result = UserService.login(db, login_in)
    return SuccessResponse(data=result, msg="登录成功")
