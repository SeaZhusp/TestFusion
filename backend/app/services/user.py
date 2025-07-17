from datetime import datetime

from app.core.dependencies.auth import Auth
from app.core.enums import UserStatus
from app.core.global_exc import CustomException
from app.crud.user import UserDal
from app.models.user import User
from app.params.user import UserParams
from app.schemas.user import UserCreateIn, LoginIn, UserOut
from app.utils.login_manage import LoginManage


class UserService:

    @staticmethod
    async def login(auth: Auth, data: LoginIn):
        user = await UserDal(auth.db).get_data(username=data.username, v_return_none=True)
        if not user:
            raise CustomException(status_code=400, msg="用户不存在")
        result = User.verify_password(data.password, user.password)
        if not result:
            raise CustomException(status_code=400, msg="密码错误")
        if user.status != UserStatus.ENABLE.value:
            raise CustomException(status_code=400, msg="用户被禁用")
        update_data = {"last_login_time": datetime.now(), "login_ip": auth.request.client.host}
        await UserDal(auth.db).put_data(user.id, update_data)
        token = LoginManage.create_token(data={"sub": str(user.id), "username": user.username})
        return {"token": token}

    @staticmethod
    async def create_user(auth: Auth, data: UserCreateIn):
        obj = await UserDal(auth.db).get_data(username=data.username, v_return_none=True)
        if obj:
            raise CustomException(status_code=400, msg="用户已存在")
        data.password = User.get_password_hash(data.password)
        user = await UserDal(auth.db).create_data(data)
        return await UserDal(auth.db).serialize(user)

    @staticmethod
    async def get_list(auth: Auth, params: UserParams):
        datas, count = await UserDal(auth.db).get_datas(**params.dict(), v_schema=UserOut, v_return_count=True)
        return datas, count
