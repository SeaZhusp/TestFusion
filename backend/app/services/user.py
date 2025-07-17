from sqlalchemy.ext.asyncio import AsyncSession

from app.core.enums import UserStatus
from app.core.global_exc import CustomException
from app.crud.user import UserDal
from app.models.user import User
from app.schemas.user import UserCreateIn, LoginIn
from app.utils.login_manage import LoginManage


class UserService:

    @staticmethod
    async def login(db: AsyncSession, data: LoginIn):
        user = await UserDal(db).get_data(username=data.username, v_return_none=True)
        if not user:
            raise CustomException(status_code=400, msg="用户不存在")
        result = User.verify_password(data.password, user.password)
        if not result:
            raise CustomException(status_code=400, msg="密码错误")
        if user.status != UserStatus.ENABLE.value:
            raise CustomException(status_code=400, msg="用户被禁用")
        token = LoginManage.create_token(data={"sub": str(user.id), "username": user.username})
        return {"token": token}

    @staticmethod
    async def create_user(db: AsyncSession, data: UserCreateIn):
        obj = await UserDal(db).get_data(username=data.username, v_return_none=True)
        if obj:
            raise CustomException(status_code=400, msg="用户已存在")
        data.password = User.get_password_hash(data.password)
        user = await UserDal(db).create_data(data)
        return await UserDal(db).serialize(user)
