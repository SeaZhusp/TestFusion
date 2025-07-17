from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import BaseDal
from app.models.user import User
from app.schemas.user import UserOut


class UserDal(BaseDal):
    def __init__(self, db: AsyncSession):
        super().__init__(db)
        self.model = User
        self.schema = UserOut
