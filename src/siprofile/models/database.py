from motor.motor_asyncio import AsyncIOMotorClient
from ..config.global_config import MONGODB_URL

client = AsyncIOMotorClient(MONGODB_URL)
db = client.siprofile_database
users_collection = db.users
cards_collection = db.cards
files_collection = db.files
