import datetime
import logging
import os

import motor.motor_tornado
# import pymongo

from aiogram.utils.exceptions import BotBlocked, BotKicked, UserDeactivated
from dotenv import load_dotenv


load_dotenv()

# Main telegram bot configs
BOT_TOKEN = os.getenv("BOT_TOKEN")


# Telegram chats
# ADMIN_IDS = tuple(os.getenv("ADMIN_IDS").split(","))
# GROUP_ID = int(os.getenv("GROUP_ID"))

# Database
MONGO_URL = os.getenv("MONGO_URL")
# cluster = pymongo.MongoClient(MONGO_URL)
cluster = motor.motor_tornado.MotorClient(MONGO_URL)
collusers = cluster.uzwikichat.users


# Telegam supported types
all_content_types = ("text", "sticker", "photo",
                     "voice", "document", "video", "video_note")


ignore_links = ('wikistipendiya', 'uzbekwikipedia')


# Logging
if not os.getenv("DEBUG"):
    formatter = '[%(asctime)s] %(levelname)8s --- %(message)s (%(filename)s:%(lineno)s)'
    logging.basicConfig(
        filename=f'logs/bot-from-{datetime.datetime.now().date()}.log',
        filemode='w',
        format=formatter,
        datefmt='%Y-%m-%d %H:%M:%S',
        level=logging.WARNING
    )


# On start polling telegram this function running
async def on_startup(dp):
    logging.warning("BOT ARE STARTED")


# On stop polling Telegram, this function running and stopping polling's
async def on_shutdown(dp):
    logging.warning("Shutting down..")
    await dp.storage.close()
    await dp.storage.wait_closed()
    logging.warning("Bye!")
