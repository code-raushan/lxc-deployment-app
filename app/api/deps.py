from fastapi import Depends

from app.core.config import get_settings
from app.services.json_db import JsonDB


def get_db(settings=Depends(get_settings)) -> JsonDB:
    return JsonDB(settings.database_file)


