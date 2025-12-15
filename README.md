# CRUD Server

Modern FastAPI backend that persists CRUD data to a JSON file. Uses an opinionated project layout with dependency injection, service layer, and Pydantic models.

## Quickstart

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
uvicorn app.main:app --reload
```

The API lives at `/api`. Interactive docs: `/docs` and `/redoc`.

## Project layout

- `app/main.py` – FastAPI app setup and router inclusion
- `app/api/routes` – Route definitions
- `app/services/json_db.py` – JSON-backed storage service
- `app/schemas` – Request/response schemas
- `data/db.json` – File-based store (git-tracked for demo)

## Running tests

```bash
pytest
```

## Environment

- `DATABASE_FILE`: path to the JSON file (default `./data/db.json`)


