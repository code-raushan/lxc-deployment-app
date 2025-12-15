from datetime import datetime
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class ItemBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=1000)
    price: float = Field(..., ge=0)


class ItemCreate(ItemBase):
    pass


class ItemUpdate(ItemBase):
    name: str | None = Field(default=None, min_length=1, max_length=200)
    price: float | None = Field(default=None, ge=0)


class ItemInDB(ItemBase):
    id: UUID = Field(default_factory=uuid4)
    created_at: datetime
    updated_at: datetime


class ItemPublic(ItemInDB):
    pass


