from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies.database import db_getter
from app.core.response import SuccessResponse
from app.schemas.user import LoginIn, UserCreateIn
from app.services.user import UserService

router = APIRouter(prefix="/user")


@router.post("/login")
async def login(
        data: LoginIn,
        db: AsyncSession = Depends(db_getter)
):
    result = await UserService.login(db, data)
    return SuccessResponse(data=result, msg="登录成功")


@router.post("/register")
async def register(
        data: UserCreateIn,
        db: AsyncSession = Depends(db_getter)
):
    result = await UserService.create_user(db, data)
    return SuccessResponse(data=result, msg="注册成功")
