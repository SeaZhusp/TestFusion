from typing import Optional

from fastapi import Request, Header, Depends

import jwt
from pydantic import BaseModel
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from app.config import settings
from app.core.dependencies.database import db_getter
from app.core.global_exc import CustomException
from starlette import status

from app.crud.user import UserDal
from app.models.user import User
from app.core.enums import UserStatus

__all__ = ["Auth", "OpenAuth", "UserAuth"]


class Auth(BaseModel):
    user: User | None = None
    db: AsyncSession
    request: Request
    data_range: int | None = None
    dept_ids: list | None = None

    class Config:
        # 接收任意类型
        arbitrary_types_allowed = True


class AuthValidation:
    """
    用于用户每次调用接口时，验证用户提交的token是否正确，并从token中获取用户信息
    """
    error_code = status.HTTP_401_UNAUTHORIZED
    warning_code = status.HTTP_400_BAD_REQUEST

    @classmethod
    def validate_token(cls, token: str | None) -> dict:
        """
        验证用户 token
        """
        if not token:
            raise CustomException(
                msg="请您先登录！",
                code=status.HTTP_403_FORBIDDEN,
                status_code=status.HTTP_403_FORBIDDEN
            )
        try:
            return jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
        except jwt.ExpiredSignatureError:
            raise CustomException(
                msg="认证已过期，请您重新登录",
                code=status.HTTP_403_FORBIDDEN,
                status_code=status.HTTP_403_FORBIDDEN
            )
        except jwt.PyJWTError:
            raise CustomException(msg="无效认证，请您重新登录", code=cls.error_code, status_code=cls.error_code)

    @classmethod
    async def validate_user(cls, request: Request, user: User, db: AsyncSession, is_all: bool = True) -> Auth:
        """
        验证用户信息
        :param request:
        :param user:
        :param db:
        :param is_all: 是否所有人访问，不加权限
        :return:
        """
        if user is None:
            raise CustomException(msg="未认证，请您重新登陆", code=cls.error_code, status_code=cls.error_code)
        elif user.status == UserStatus.DISABLE.value:
            raise CustomException(msg="用户已被冻结！", code=cls.error_code, status_code=cls.error_code)
        request.scope["username"] = user.username
        request.scope["user_id"] = user.id
        request.scope["fullname"] = user.fullname
        try:
            request.scope["body"] = await request.body()
        except RuntimeError:
            request.scope["body"] = "获取失败"
        if is_all:
            return Auth(user=user, db=db, request=request)
        data_range, dept_ids = await cls.get_user_data_range(user, db)
        return Auth(user=user, db=db, request=request, data_range=data_range, dept_ids=dept_ids)

    @classmethod
    def get_user_permissions(cls, user: User) -> set:
        """
        获取员工用户所有权限列表
        :param user: 用户实例
        :return:
        """
        return {'*.*.*'}
        # if user.user_type == UserType.ADMIN.value:
        #     return {'*.*.*'}
        # permissions = set()
        # for role_obj in user.roles:
        #     for menu in role_obj.menus:
        #         if menu.perms and not menu.disabled:
        #             permissions.add(menu.perms)
        # return permissions

    @classmethod
    async def get_user_data_range(cls, user: User, db: AsyncSession) -> tuple:
        """
        获取用户数据范围
        0 仅本人数据权限  create_user_id 查询
        1 本部门数据权限  部门 id 左连接查询
        2 本部门及以下数据权限 部门 id 左连接查询
        3 自定义数据权限  部门 id 左连接查询
        4 全部数据权限  无
        :param user:
        :param db:
        :return:
        """
        return 4, ["*"]
        # if user.user_type == UserType.ADMIN.value:
        #     return 4, ["*"]
        # data_range = max([i.data_range for i in user.roles])
        # dept_ids = set()
        # if data_range == 0:
        #     pass
        # elif data_range == 1:
        #     for dept in user.depts:
        #         dept_ids.add(dept.id)
        # elif data_range == 2:
        #     # 递归获取部门列表
        #     dept_ids = await UserDal(db).recursion_get_dept_ids(user)
        # elif data_range == 3:
        #     for role_obj in user.roles:
        #         for dept in role_obj.depts:
        #             dept_ids.add(dept.id)
        # elif data_range == 4:
        #     dept_ids.add("*")
        # return data_range, list(dept_ids)


class OpenAuth(AuthValidation):
    """开放认证"""

    async def __call__(
            self,
            request: Request,
            token: Optional[str] = Header(default=None),
            db: AsyncSession = Depends(db_getter)
    ):
        return Auth(db=db, request=request)


class UserAuth(AuthValidation):
    """
    用户认证
    获取员工用户完整信息
    如果有权限，那么会验证该用户是否包括权限列表中的其中一个权限
    """

    def __init__(self, permissions: list[str] | None = None):
        if permissions:
            self.permissions = set(permissions)
        else:
            self.permissions = None

    async def __call__(
            self,
            request: Request,
            token: Optional[str] = Header(default=None),
            db: AsyncSession = Depends(db_getter)
    ) -> Auth:
        username = self.validate_token(token)["username"]
        # options = [joinedload(SysUser.roles).subqueryload(SysRole.menus), joinedload(SysUser.depts)]
        # user = await UserDal(db).get_data(username=username, v_return_none=True, v_options=options)
        user = await UserDal(db).get_data(username=username, v_return_none=True)
        result = await self.validate_user(request, user, db, is_all=False)
        # permissions = self.get_user_permissions(user)
        # if permissions != {'*.*.*'} and self.permissions:
        #     if not (self.permissions & permissions):
        #         raise CustomException(msg="无权限操作", code=status.HTTP_403_FORBIDDEN)
        return result
