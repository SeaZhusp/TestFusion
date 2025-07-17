from fastapi import APIRouter, Depends

from app.core.dependencies.auth import Auth, UserAuth
from app.core.response import SuccessResponse
from app.params.user import UserParams
from app.services.user import UserService

router = APIRouter(prefix="/users")


@router.get("/", summary="获取用户列表")
async def get_list(
        params: UserParams = Depends(),
        auth: Auth = Depends(UserAuth())
):
    datas, count = await UserService.get_list(auth, params)
    return SuccessResponse(datas, count=count, msg="获取用户列表成功")
