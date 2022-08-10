from os import environ as env

from dotenv import load_dotenv

load_dotenv("config.env")

"""
READ EVERYTHING CAREFULLY!!!
"""


DEPLOYING_ON_HEROKU = (
    False  # Make this False if you're not deploying On heroku/Docker
)


if not DEPLOYING_ON_HEROKU:
    BOT_TOKEN = "5442868128:AAH18gxDfJny0VNkUjYp9S3Xi9X08ovaNmY"
    SUDOERS = [5545068262]
    MONGO_DB_URL = "mongodb+srv://spam:spam@cluster0.2vykm.mongodb.net/?retryWrites=true&w=majority"
else:
    BOT_TOKEN = env.get("BOT_TOKEN", "5442868128:AAH18gxDfJny0VNkUjYp9S3Xi9X08ovaNmY")
    SUDOERS = [int(x) for x in env.get("SUDO_USERS_ID", "5545068262").split()]
    MONGO_DB_URL = env.get("MONGO_DB_URL", "mongodb+srv://spam:spam@cluster0.2vykm.mongodb.net/?retryWrites=true&w=majority")
  
