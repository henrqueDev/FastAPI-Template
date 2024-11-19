from typing import Union
from pydantic import BaseModel
from sqlmodel import SQLModel, Field

class User(SQLModel, table=True):
    id: Union[int, None] = Field(default=None, primary_key=True)
    username: str = Field(index=True)
    email: Union[str, None] = Field(default = None)
    full_name: Union[str, None] = Field(default = None)
    disabled: Union[bool, None] = Field(default = None)
    hashed_password: str


