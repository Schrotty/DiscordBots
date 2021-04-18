import os

from discord import Intents
from dotenv import load_dotenv, find_dotenv

from core.paperbot import Paperbot

if __name__ == "__main__":
    if load_dotenv(find_dotenv(f"configuration/.{os.getenv('ENVIRONMENT')}.env")):
        Paperbot(command_prefix=[os.getenv('PAPERBOT.BOT.PREFIX')], intents=Intents.all()).boot()
