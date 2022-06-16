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
    BOT_TOKEN = "5557458280:AAGqsLMWO9KcHOk2JJwZSlH7o-raX_GLH9Q"
    SUDOERS = [5545068262]
    NSFW_LOG_CHANNEL = "-1001667411233"
    SPAM_LOG_CHANNEL = "-1001667411233"
    ARQ_API_KEY = "LQIHOH-OYUWTI-ZXHYNM-GDEBOB-ARQ"  # Get it from @ARQRobot
else:
    BOT_TOKEN = env.get("BOT_TOKEN", "5557458280:AAGqsLMWO9KcHOk2JJwZSlH7o-raX_GLH9Q")
    SUDOERS = [int(x) for x in env.get("SUDO_USERS_ID", "5545068262").split()]
    NSFW_LOG_CHANNEL = int(env.get("NSFW_LOG_CHANNEL", "-1001667411233"))
    SPAM_LOG_CHANNEL = int(env.get("SPAM_LOG_CHANNEL", "-1001667411233"))
    ARQ_API_KEY = env.get("ARQ_API_KEY", "LQIHOH-OYUWTI-ZXHYNM-GDEBOB-ARQ")