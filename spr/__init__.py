from os.path import exists
from pyrogram import Client

API_ID = 6
API_HASH = "eb06d4abfb49dc3eeb1aeb98ae0f581e"

if exists("config.py"):
    from config import *
else:
    from sample_config import *

spr = Client(
    name="spr",
    bot_token=BOT_TOKEN,
    api_id=API_ID,
    api_hash=API_HASH,
)
with spr:
    bot = spr.get_me()
    BOT_ID = bot.id
    BOT_USERNAME = bot.username
