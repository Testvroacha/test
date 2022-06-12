from os import environ as env

from dotenv import load_dotenv

load_dotenv("config.env")

"""
READ EVERYTHING CAREFULLY!!!
"""


DEPLOYING_ON_HEROKU = (
    True  # Make this False if you're not deploying On heroku/Docker
)


if not DEPLOYING_ON_HEROKU:
    BOT_TOKEN = ""
    SUDOERS = []
    NSFW_LOG_CHANNEL = ""
    SPAM_LOG_CHANNEL = ""
    ARQ_API_KEY = ""  # Get it from @ARQRobot
else:
    BOT_TOKEN = env.get("BOT_TOKEN", "5557458280:AAFXz2_xxG_hhsYS3rXY2fTN6E9yXAKRMsQ")
    SUDOERS = [int(x) for x in env.get("SUDO_USERS_ID", "5545068262").split()]
    NSFW_LOG_CHANNEL = int(env.get("NSFW_LOG_CHANNEL", "-1001667411233"))
    SPAM_LOG_CHANNEL = int(env.get("SPAM_LOG_CHANNEL", "-1001667411233"))
    ARQ_API_KEY = env.get("ARQ_API_KEY", "GBGOGP-ZAUTAU-IJCFGH-GFDZQT-ARQ")
