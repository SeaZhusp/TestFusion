from sqlalchemy import Column, String, SMALLINT, text, DateTime

from app.models.base import BaseModel


class SystemUser(BaseModel):
    __tablename__ = "system_user"

    username = Column(String(255), nullable=False, server_default="", comment="用户名")
    password = Column(String(255), nullable=False, server_default="", comment="密码")
    fullname = Column(String(255), nullable=False, server_default="", comment="姓名")
    email = Column(String(255), nullable=False, server_default="", comment="邮箱")
    mobile = Column(String(255), nullable=False, server_default="", comment="手机号")
    gender = Column(SMALLINT, nullable=False, server_default=text('0'), comment="性别：1-男, 2-女")
    status = Column(SMALLINT, nullable=False, server_default=text('1'), comment="状态：1-正常, 2-禁用")
    last_login_time = Column(DateTime, nullable=True, comment="最后登录时间")
    last_login_ip = Column(String(255), nullable=False, server_default="", comment="最后登录IP")
    is_delete = Column(SMALLINT, nullable=False, server_default=text('0'), comment="是否删除：0-否, 1-是")
