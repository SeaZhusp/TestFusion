from pydantic import BaseModel, Field


class UserBase(BaseModel):
    fullname: str = Field(..., min_length=3, max_length=50)
    username: str = Field(..., min_length=3, max_length=50)

    class Config:
        from_attributes = True


class UserCreateIn(UserBase):
    password: str = Field(..., min_length=6, max_length=50)


class UserOut(UserBase):
    id: int = Field(...)


class LoginIn(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6, max_length=50)
