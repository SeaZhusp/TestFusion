from fastapi import APIRouter, Depends

from app.core.dependencies.auth import OpenAuth, Auth
from app.core.response import SuccessResponse
from app.schemas.auth import LoginIn, UserRegisterIn
from app.services.auth import AuthService

router = APIRouter(prefix="/auth")


@router.post("/login", summary="用户登录")
async def login(
        data: LoginIn,
        auth: Auth = Depends(OpenAuth())
):
    result = await AuthService.login(auth, data)
    return SuccessResponse(data=result, msg="登录成功")


@router.post("/register", summary="用户注册")
async def register(
        data: UserRegisterIn,
        auth: Auth = Depends(OpenAuth())
):
    result = await AuthService.register(auth, data)
    return SuccessResponse(data=result, msg="注册成功")
