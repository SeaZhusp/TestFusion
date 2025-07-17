from fastapi import APIRouter, Depends

from app.core.dependencies.auth import OpenAuth, Auth, UserAuth
from app.core.response import SuccessResponse
from app.params.user import UserParams
from app.schemas.user import LoginIn, UserCreateIn
from app.services.user import UserService

router = APIRouter(prefix="/user")


@router.post("/login", summary="用户登录")
async def login(
        data: LoginIn,
        auth: Auth = Depends(OpenAuth())
):
    result = await UserService.login(auth, data)
    return SuccessResponse(data=result, msg="登录成功")


@router.post("/register", summary="用户注册")
async def register(
        data: UserCreateIn,
        auth: Auth = Depends(OpenAuth())
):
    result = await UserService.create_user(auth, data)
    return SuccessResponse(data=result, msg="注册成功")


@router.get("/list", summary="获取用户列表")
async def get_list(
        params: UserParams = Depends(),
        auth: Auth = Depends(UserAuth())
):
    datas, count = await UserService.get_list(auth, params)
    return SuccessResponse(datas, count=count, msg="获取用户列表成功")
