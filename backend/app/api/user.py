from fastapi import APIRouter, Depends

from app.core.dependencies.auth import Auth, UserAuth
from app.core.response import SuccessResponse
from app.params.user import UserParams
from app.schemas.user import UserUpdateIn, UserUpdateStatusIn, AdminPasswordResetIn, UserPasswordUpdateIn
from app.services.user import UserService

router = APIRouter(prefix="/users")


@router.get("/", summary="获取用户列表")
async def get_users(
        params: UserParams = Depends(),
        auth: Auth = Depends(UserAuth())
):
    datas, count = await UserService.get_users(auth, params)
    return SuccessResponse(datas, count=count, msg="获取用户列表成功")


@router.get("/{user_id}", summary="获取用户信息")
async def get_user(
        user_id: int,
        auth: Auth = Depends(UserAuth())
):
    data = await UserService.get_user(auth, user_id)
    return SuccessResponse(data, msg="获取用户信息成功")


@router.put("/{user_id}", summary="更新用户信息")
async def update_user(
        user_id: int,
        data: UserUpdateIn,
        auth: Auth = Depends(UserAuth())
):
    data = await UserService.update_user(auth, user_id, data)
    return SuccessResponse(data, msg="更新用户信息成功")


@router.delete("/{user_id}", summary="删除用户")
async def delete_user(
        user_id: int,
        auth: Auth = Depends(UserAuth())
):
    await UserService.delete_user(auth, user_id)
    return SuccessResponse(msg="删除用户成功")


@router.put("/{user_id}/status", summary="更新用户状态")
async def update_user_status(
        user_id: int,
        data: UserUpdateStatusIn,
        auth: Auth = Depends(UserAuth())
):
    await UserService.update_user_status(auth, user_id, data)
    return SuccessResponse(msg="更新用户状态成功")


@router.put("/{user_id}/password/reset", summary="管理员重置用户密码")
async def reset_user_password(
        user_id: int,
        data: AdminPasswordResetIn,
        auth: Auth = Depends(UserAuth())
):
    await UserService.reset_user_password(auth, user_id, data.new_password)
    return SuccessResponse(msg="密码重置成功")


@router.put("/password", summary="用户修改自己密码")
async def update_user_password(
        data: UserPasswordUpdateIn,
        auth: Auth = Depends(UserAuth())
):
    await UserService.update_user_password(auth, auth.user.id, data)
    return SuccessResponse(msg="密码修改成功")
