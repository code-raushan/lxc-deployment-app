from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class Item:
    id: UUID
    name: str
    description: str | None
    price: float
    created_at: datetime
    updated_at: datetime


