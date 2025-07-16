from enum import IntEnum


class UserStatus(IntEnum):
    """
    用户状态枚举: 1-启用, 2-禁用
    """
    ENABLE = 1
    DISABLE = 2


class UserType(IntEnum):
    """
    用户权限枚举: 0-普通用户, 1-管理员
    """
    USER = 0
    ADMIN = 1


class DeleteStatus(IntEnum):
    """
    删除状态枚举: 0-未删除, 1-已删除
    """
    NO = 0
    YES = 1
