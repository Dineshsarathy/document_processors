# from motor.motor_asyncio import AsyncIOMotorClient, 
# from app.core.config import settings

# client = AsyncIOMotorClient(settings.mongodb_url)
# db = client[settings.mongodb_name]

# def get_database() -> AsyncIOMotorClient:
#     return db

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from app.core.config import settings

client = AsyncIOMotorClient(settings.mongodb_url)
db = client[settings.mongodb_name]

def get_database() -> AsyncIOMotorDatabase:
    return db
