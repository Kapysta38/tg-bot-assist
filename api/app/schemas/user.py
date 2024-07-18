from typing import Optional, Union
from datetime import datetime

from pydantic import BaseModel


class UserBase(BaseModel):
    tg_id: int
    username: Union[str, None]


class UserCreate(UserBase):
    pass


class UserUpdate(UserBase):
    tg_id: Optional[int] = None
    username: Union[str, None] = None


class UserInDBBase(UserBase):
    user_id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

