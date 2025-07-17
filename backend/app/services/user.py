from app.core.dependencies.auth import Auth
from app.crud.user import UserDal
from app.params.user import UserParams
from app.schemas.user import UserOut, UserUpdateIn


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
