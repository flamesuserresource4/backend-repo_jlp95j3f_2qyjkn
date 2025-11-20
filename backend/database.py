import os
from typing import Any, Dict, List, Optional
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "appdb")

_client: Optional[AsyncIOMotorClient] = None
_db: Optional[AsyncIOMotorDatabase] = None

async def get_db() -> AsyncIOMotorDatabase:
    global _client, _db
    if _db is None:
        _client = AsyncIOMotorClient(DATABASE_URL)
        _db = _client[DATABASE_NAME]
    return _db

async def create_document(collection: str, data: Dict[str, Any]) -> str:
    db = await get_db()
    payload = {**data, "_created_at": os.times()[-1]}
    result = await db[collection].insert_one(payload)
    return str(result.inserted_id)

async def get_documents(collection: str, filter_dict: Dict[str, Any] | None = None, limit: int = 50) -> List[Dict[str, Any]]:
    db = await get_db()
    cursor = db[collection].find(filter_dict or {}).limit(limit)
    out: List[Dict[str, Any]] = []
    async for doc in cursor:
        doc["_id"] = str(doc["_id"])  # stringify ObjectId
        out.append(doc)
    return out
