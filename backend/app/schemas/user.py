from pydantic import BaseModel, Field


class User(BaseModel):
    name: str = Field(..., min_length=3, max_length=50)
    username: str = Field(..., min_length=3, max_length=50)


class UserCreateIn(User):
    password: str = Field(..., min_length=8, max_length=50)


class UserOut(User):
    id: int = Field(...)
