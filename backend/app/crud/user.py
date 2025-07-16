from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import BaseDal


class UserDal(BaseDal):
    def __init__(self, db: AsyncSession):
        super().__init__(db)
