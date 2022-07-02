from motor.motor_asyncio import AsyncIOMotorClient as Bot
from spr import MONGO_DB_URL as tmo


MONGODB_CLI = Bot(tmo)
db = MONGODB_CLI.program




