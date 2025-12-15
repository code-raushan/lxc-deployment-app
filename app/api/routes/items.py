from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps import get_db
from app.schemas.item import ItemCreate, ItemPublic, ItemUpdate
from app.services.json_db import JsonDB

router = APIRouter(prefix="/items", tags=["items"])


@router.get("", response_model=list[ItemPublic])
async def list_items(db: JsonDB = Depends(get_db)) -> list[ItemPublic]:
    return await db.list_items()


@router.post("", response_model=ItemPublic, status_code=status.HTTP_201_CREATED)
async def create_item(data: ItemCreate, db: JsonDB = Depends(get_db)) -> ItemPublic:
    return await db.create_item(data)


@router.get("/{item_id}", response_model=ItemPublic)
async def get_item(item_id: UUID, db: JsonDB = Depends(get_db)) -> ItemPublic:
    item = await db.get_item(item_id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return item


@router.put("/{item_id}", response_model=ItemPublic)
async def update_item(
    item_id: UUID, data: ItemUpdate, db: JsonDB = Depends(get_db)
) -> ItemPublic:
    item = await db.update_item(item_id, data)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(item_id: UUID, db: JsonDB = Depends(get_db)) -> None:
    deleted = await db.delete_item(item_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")


