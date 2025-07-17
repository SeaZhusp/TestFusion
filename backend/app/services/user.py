from app.core.dependencies.auth import Auth
from app.crud.user import UserDal
from app.params.user import UserParams
from app.schemas.user import UserOut


class UserService:

    @staticmethod
    async def get_list(auth: Auth, params: UserParams):
        datas, count = await UserDal(auth.db).get_datas(**params.dict(), v_schema=UserOut, v_return_count=True)
        return datas, count
