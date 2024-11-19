from typing import Union
from pydantic import BaseModel
from sqlmodel import Field, SQLModel

class Item(SQLModel, table=True):
    id: Union[int, None] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    description: Union[str , None] = None
    price: float
    tax: Union[float , None] = None