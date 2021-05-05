import logging
import os

from pony.orm import Database

# create database object and establish connection
database: Database = Database()
database.bind(
    provider="mysql",
    host=os.getenv("PAPERBOT.DATABASE.HOST"),
    user=os.getenv("PAPERBOT.DATABASE.USER"),
    passwd=os.getenv("PAPERBOT.DATABASE.PASSWD"),
    db=os.getenv("PAPERBOT.DATABASE.DB"),
    charset="utf8mb4",
)

# create logs folder
if not os.path.exists("logs/"):
    os.mkdir("logs/")

# discord log config
handler = logging.FileHandler(filename="logs/discord.log", encoding="utf-8", mode="w")
handler.setFormatter(logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s"))

logger = logging.getLogger("discord")
logger.addHandler(handler)

# paperbot log config
handler = logging.FileHandler(filename="logs/paperbot.log", encoding="utf-8", mode="w")
handler.setFormatter(logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s"))

logger = logging.getLogger("paperbot")
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)
