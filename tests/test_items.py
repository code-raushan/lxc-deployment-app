from pathlib import Path

import pytest
from fastapi import status
from httpx import AsyncClient

from app.api.deps import get_db
from app.main import create_application
from app.services.json_db import JsonDB


@pytest.fixture()
def tmp_db(tmp_path: Path) -> Path:
    db_path = tmp_path / "db.json"
    db_path.write_text("[]", encoding="utf-8")
    return db_path


@pytest.fixture()
def app(tmp_db: Path):
    application = create_application()
    # Patch dependency manually since we do not use overrides here
    application.dependency_overrides[get_db] = lambda: JsonDB(tmp_db)
    return application


@pytest.mark.asyncio()
async def test_crud_flow(app):
    async with AsyncClient(app=app, base_url="http://test") as client:
        create_resp = await client.post(
            "/api/items",
            json={"name": "Sample", "price": 10.5, "description": "Demo"},
        )
        assert create_resp.status_code == status.HTTP_201_CREATED
        created = create_resp.json()

        get_resp = await client.get(f"/api/items/{created['id']}")
        assert get_resp.status_code == status.HTTP_200_OK

        list_resp = await client.get("/api/items")
        assert list_resp.status_code == status.HTTP_200_OK
        assert len(list_resp.json()) == 1

        update_resp = await client.put(
            f"/api/items/{created['id']}",
            json={"name": "Updated", "price": 11.0, "description": "Updated desc"},
        )
        assert update_resp.status_code == status.HTTP_200_OK
        assert update_resp.json()["name"] == "Updated"

        delete_resp = await client.delete(f"/api/items/{created['id']}")
        assert delete_resp.status_code == status.HTTP_204_NO_CONTENT

        missing_resp = await client.get(f"/api/items/{created['id']}")
        assert missing_resp.status_code == status.HTTP_404_NOT_FOUND


