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
    BOT_TOKEN = "5557458280:AAGgGDhmEAwkK4BFy31ILAUxVrPFBa2UDD8"
    SUDOERS = [5545068262]
    ARQ_API_KEY = "SCQEDR-KAVRFC-SPYXEK-MVUKWI-ARQ"
    MONGO_DB_URL = "mongodb+srv://spam:spam@cluster0.2vykm.mongodb.net/?retryWrites=true&w=majority"
    SPAM_LOG_CHANNEL = -1001667411233
else:
    BOT_TOKEN = env.get("BOT_TOKEN", "5557458280:AAGgGDhmEAwkK4BFy31ILAUxVrPFBa2UDD8")
    SUDOERS = [int(x) for x in env.get("SUDO_USERS_ID", "5545068262").split()]
    MONGO_DB_URL = env.get("MONGO_DB_URL", "mongodb+srv://spam:spam@cluster0.2vykm.mongodb.net/?retryWrites=true&w=majority")
    SPAM_LOG_CHANNEL = int(env.get("SPAM_LOG_CHANNEL", "-1001667411233"))
    ARQ_API_KEY = env.get("ARQ_API_KEY", "SCQEDR-KAVRFC-SPYXEK-MVUKWI-ARQ")
