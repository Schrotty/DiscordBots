import logging
import os

# create logs folder
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