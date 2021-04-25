import logging


def setup():
    paperlog = logging.getLogger("paperbot")
    paperlog.setLevel(logging.INFO)

    logger = logging.getLogger("discord")
    logger.setLevel(logging.DEBUG)

    handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")
    handler.setFormatter(
        logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s")
    )
    logger.addHandler(handler)
