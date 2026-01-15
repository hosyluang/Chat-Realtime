from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    username: str
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None


# schema nay de phia FE gui len
class UserCreate(UserBase):
    password: str


# schema nay de cho BE response ve cho FE va ko gui pw
class UserResponse(UserBase):
    id: int
    avatar_url: Optional[str] = None
    created_at: datetime
    is_active: bool

    class Config:
        # Cho phep pydantic doc du lieu tu models
        from_attributes = True
