from app.core.dependencies.auth import Auth
from app.core.global_exc import CustomException
from app.crud.user import UserDal
from app.models.user import User
from app.params.user import UserParams
from app.schemas.user import UserOut, UserUpdateIn, UserUpdateStatusIn, AdminPasswordResetIn, UserPasswordUpdateIn


class UserService:

    @staticmethod
    async def get_users(auth: Auth, params: UserParams):
        datas, count = await UserDal(auth.db).get_datas(**params.dict(), v_schema=UserOut, v_return_count=True)
        return datas, count

    @staticmethod
    async def get_user(auth: Auth, user_id: int):
        data = await UserDal(auth.db).get_data(id=user_id, v_schema=UserOut)
        return data

    @staticmethod
    async def update_user(auth: Auth, user_id: int, data: UserUpdateIn):
        user = await UserDal(auth.db).put_data(data_id=user_id, data=data)
        return user

    @staticmethod
    async def delete_user(auth: Auth, user_id: int):
        await UserDal(auth.db).delete_datas(ids=[user_id])

    @staticmethod
    async def update_user_status(auth: Auth, user_id: int, data: UserUpdateStatusIn):
        user = await UserDal(auth.db).get_data(user_id, v_return_none=True)
        if not user:
            raise CustomException(msg="用户不存在")
        if user_id == auth.user.id:
            raise CustomException(msg="不能修改自己的状态")
        result = await UserDal(auth.db).put_data(user_id, data)
        return result

    @staticmethod
    async def reset_user_password(auth: Auth, user_id: int, data: AdminPasswordResetIn):
        user = await UserDal(auth.db).get_data(user_id)
        if not user:
            raise CustomException(msg="用户不存在")
        hashed_password = User.get_password_hash(data.password)
        update_data = {"password": hashed_password}
        result = await UserDal(auth.db).put_data(user_id, update_data)
        return result

    @staticmethod
    async def update_user_password(auth: Auth, data: UserPasswordUpdateIn):
        try:
            data.validate_passwords()
        except ValueError as e:
            raise CustomException(msg=str(e))
        user = await UserDal(auth.db).get_data(auth.user.id)
        if not User.verify_password(data.old_password, user.password):
            raise CustomException(msg="旧密码错误")
        hashed_password = User.get_password_hash(data.new_password)
        update_data = {"password": hashed_password}
        result = await UserDal(auth.db).put_data(auth.user.id, update_data)
        return result
