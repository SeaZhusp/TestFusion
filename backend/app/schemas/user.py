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
