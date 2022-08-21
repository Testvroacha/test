from motor.motor_asyncio import AsyncIOMotorClient as Bot
from spr import MONGO_DB_URL as tmo
from typing import Dict, List, Union



MONGODB_CLI = Bot(tmo)
db = MONGODB_CLI.program

gbansdb = db.gban

async def get_gbans_count() -> int:
    users = gbansdb.find({"user_id": {"$gt": 0}})
    users = await users.to_list(length=100000)
    return len(users)


async def is_gbanned_user(user_id: int) -> bool:
    user = await gbansdb.find_one({"user_id": user_id})
    if not user:
        return False
    return True


async def add_gban_user(user_id: int):
    is_gbanned = await is_gbanned_user(user_id)
    if is_gbanned:
        return
    return await gbansdb.insert_one({"user_id": user_id})


async def remove_gban_user(user_id: int):
    is_gbanned = await is_gbanned_user(user_id)
    if not is_gbanned:
        return
    return await gbansdb.delete_one({"user_id": user_id})


blacklist_chatdb = db.blacklistChat


async def blacklisted_chats() -> list:
    chats = blacklist_chatdb.find({"chat_id": {"$lt": 0}})
    return [
        chat["chat_id"] for chat in await chats.to_list(length=1000000000)
    ]


async def black_chat(chat_id: int) -> bool:
    if not await blacklist_chatdb.find_one({"chat_id": chat_id}):
        await blacklist_chatdb.insert_one({"chat_id": chat_id})
        return True
    return False


async def white_chat(chat_id: int) -> bool:
    if await blacklist_chatdb.find_one({"chat_id": chat_id}):
        await blacklist_chatdb.delete_one({"chat_id": chat_id})
        return True
    return False


async def is_black_chat(chat_id: int) -> bool:
    chat = await blacklist_chatdb.find_one({"chat_id": chat_id})
    if not chat:
        return False
    return True


usersdb = db.users


async def is_served_user(user_id: int) -> bool:
    user = await usersdb.find_one({"user_id": user_id})
    if not user:
        return False
    return True


async def get_served_users() -> list:
    users = usersdb.find({"user_id": {"$gt": 0}})
    if not users:
        return []
    users_list = []
    for user in await users.to_list(length=1000000000):
        users_list.append(user)
    return users_list


async def add_served_user(user_id: int):
    is_served = await is_served_user(user_id)
    if is_served:
        return
    return await usersdb.insert_one({"user_id": user_id})



chatsdb = db.chats


async def get_served_chats() -> list:
    chats = chatsdb.find({"chat_id": {"$lt": 0}})
    if not chats:
        return []
    chats_list = []
    for chat in await chats.to_list(length=1000000000):
        chats_list.append(chat)
    return chats_list


async def is_served_chat(chat_id: int) -> bool:
    chat = await chatsdb.find_one({"chat_id": chat_id})
    if not chat:
        return False
    return True


async def add_served_chat(chat_id: int):
    is_served = await is_served_chat(chat_id)
    if is_served:
        return
    return await chatsdb.insert_one({"chat_id": chat_id})


async def remove_served_chat(chat_id: int):
    is_served = await is_served_chat(chat_id)
    if not is_served:
        return
    return await chatsdb.delete_one({"chat_id": chat_id})



porndb = db.porn


async def get_porn_chats() -> list:
    chats = porndb.find({"chat_id": {"$lt": 0}})
    if not chats:
        return []
    chats_list = []
    for chat in await chats.to_list(length=1000000000):
        chats_list.append(chat)
    return chats_list


async def is_nsfw_enabled(chat_id: int) -> bool:
    chat = await porndb.find_one({"chat_id": chat_id})
    if not chat:
        return False
    return True


async def enable_nsfw(chat_id: int):
    is_porn = await is_nsfw_enabled(chat_id)
    if is_porn:
        return
    return await porndb.insert_one({"chat_id": chat_id})


async def disable_nsfw(chat_id: int):
    is_porn = await is_nsfw_enabled(chat_id)
    if not is_porn:
        return
    return await porndb.delete_one({"chat_id": chat_id})



admindb = db.admin


async def get_admin_chats() -> list:
    chats = admindb.find({"chat_id": {"$lt": 0}})
    if not chats:
        return []
    chats_list = []
    for chat in await chats.to_list(length=1000000000):
        chats_list.append(chat)
    return chats_list


async def is_admin_chat(chat_id: int) -> bool:
    chat = await admindb.find_one({"chat_id": chat_id})
    if not chat:
        return False
    return True


async def enable_admin(chat_id: int):
    is_admin = await is_admin_chat(chat_id)
    if is_admin:
        return
    return await admindb.insert_one({"chat_id": chat_id})


async def disable_admin(chat_id: int):
    is_admin = await is_admin_chat(chat_id)
    if not is_admin:
        return
    return await admindb.delete_one({"chat_id": chat_id})


countdb = db.countnsfw

async def get_nsfw_count(user_id: int):
    _notes = await countdb.find_one({"user_id": user_id})
    if not _notes:
        return 0
    return _notes["notes"]

async def save_nsfw(user_id: int):
    await countdb.update_one(
        {"user_id": user_id}, {"$inc": {"notes": int(1)}}, upsert=True
    )

