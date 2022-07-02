from motor.motor_asyncio import AsyncIOMotorClient as Bot
from config import MONGO_DB_URL as tmo


MONGODB_CLI = Bot(tmo)
db = MONGODB_CLI.program




