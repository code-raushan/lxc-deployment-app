import asyncio
import json
from collections.abc import Iterable
from datetime import datetime, timezone
from pathlib import Path
from uuid import UUID, uuid4

from app.models.item import Item
from app.schemas.item import ItemCreate, ItemUpdate


class JsonDB:
    """Simple JSON file storage for Items."""

    def __init__(self, file_path: Path) -> None:
        self.file_path = file_path
        self._lock = asyncio.Lock()
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.file_path.exists():
            self._write_file([])

    async def list_items(self) -> list[Item]:
        rows = await self._read_file()
        return [self._deserialize(row) for row in rows]

    async def get_item(self, item_id: UUID) -> Item | None:
        items = await self.list_items()
        for item in items:
            if item.id == item_id:
                return item
        return None

    async def create_item(self, data: ItemCreate) -> Item:
        now = datetime.now(timezone.utc)
        item = Item(
            id=uuid4(),
            name=data.name,
            description=data.description,
            price=data.price,
            created_at=now,
            updated_at=now,
        )
        async with self._lock:
            items = await self.list_items()
            items.append(item)
            await self._persist(items)
        return item

    async def update_item(self, item_id: UUID, data: ItemUpdate) -> Item | None:
        async with self._lock:
            items = await self.list_items()
            updated: Item | None = None
            for idx, item in enumerate(items):
                if item.id == item_id:
                    updated = Item(
                        id=item.id,
                        name=data.name if data.name is not None else item.name,
                        description=data.description if data.description is not None else item.description,
                        price=data.price if data.price is not None else item.price,
                        created_at=item.created_at,
                        updated_at=datetime.now(timezone.utc),
                    )
                    items[idx] = updated
                    break
            if updated is None:
                return None
            await self._persist(items)
            return updated

    async def delete_item(self, item_id: UUID) -> bool:
        async with self._lock:
            items = await self.list_items()
            remaining = [item for item in items if item.id != item_id]
            if len(remaining) == len(items):
                return False
            await self._persist(remaining)
            return True

    async def _persist(self, items: Iterable[Item]) -> None:
        await self._write_file([self._serialize(item) for item in items])

    async def _read_file(self) -> list[dict]:
        return await asyncio.to_thread(self._read_json_sync)

    async def _write_file(self, payload: list[dict]) -> None:
        await asyncio.to_thread(self._write_json_sync, payload)

    def _read_json_sync(self) -> list[dict]:
        with self.file_path.open("r", encoding="utf-8") as f:
            return json.load(f)

    def _write_json_sync(self, payload: list[dict]) -> None:
        with self.file_path.open("w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2, default=str)

    def _serialize(self, item: Item) -> dict:
        return {
            "id": str(item.id),
            "name": item.name,
            "description": item.description,
            "price": item.price,
            "created_at": item.created_at.isoformat(),
            "updated_at": item.updated_at.isoformat(),
        }

    def _deserialize(self, data: dict) -> Item:
        return Item(
            id=UUID(data["id"]),
            name=data["name"],
            description=data.get("description"),
            price=float(data["price"]),
            created_at=datetime.fromisoformat(data["created_at"]),
            updated_at=datetime.fromisoformat(data["updated_at"]),
        )


