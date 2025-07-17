from typing import Optional

from pydantic import BaseModel, Field
from app.core.data_types import DatetimeStr, Email, Mobile


class UserBase(BaseModel):
    fullname: str = Field(..., min_length=1, max_length=50)
    username: str = Field(..., min_length=1, max_length=50)
    email: Optional[Email] = Field(None, max_length=50)
    mobile: Optional[Mobile] = Field(None, max_length=50)
    gender: int = Field(..., ge=0, le=2)
    user_type: int = Field(..., ge=0, le=1)
    status: int = Field(..., ge=0, le=1)
    last_login_time: Optional[DatetimeStr] = None
    last_login_ip: str = Field(..., max_length=50)
    created_at: DatetimeStr
    updated_at: DatetimeStr

    class Config:
        from_attributes = True


class UserOut(UserBase):
    id: int = Field(..., ge=1)


class UserUpdateIn(BaseModel):
    fullname: str = Field(..., min_length=1, max_length=50)
    email: Optional[Email] = Field(None, max_length=50)
    mobile: Optional[Mobile] = Field(None, max_length=50)
    gender: int = Field(..., ge=0, le=2)


class UserUpdateStatusIn(BaseModel):
    status: int = Field(..., ge=0, le=1)


class UserPasswordUpdateIn(BaseModel):
    old_password: str = Field(..., min_length=6, max_length=50)
    new_password: str = Field(..., min_length=6, max_length=50)
    confirm_password: str = Field(..., min_length=6, max_length=50)

    def validate_passwords(self):
        """验证密码"""
        if self.new_password != self.confirm_password:
            raise ValueError("新密码和确认密码不一致")
        if self.old_password == self.new_password:
            raise ValueError("新密码不能与旧密码相同")
        return True


class AdminPasswordResetIn(BaseModel):
    password: str = Field(..., min_length=6, max_length=50)
