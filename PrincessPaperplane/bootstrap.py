import os

from discord import Intents
from dotenv import load_dotenv, find_dotenv

if __name__ == "__main__":
    if load_dotenv(
        find_dotenv(f"configuration/.{os.getenv('PAPERBOT.ENVIRONMENT')}.env")
    ):
        from core.paperbot import Paperbot

        Paperbot(
            command_prefix=[os.getenv("PAPERBOT.BOT.PREFIX")], intents=Intents.all()
        ).boot()
