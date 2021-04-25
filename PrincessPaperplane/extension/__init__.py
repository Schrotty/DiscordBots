from discord.ext.commands import Bot

from utility.terminal import Terminal

EXTENSIONS = ["dice", "quotly", "wool"]


def load_extensions(bot: Bot):
    for extension in EXTENSIONS:
        bot.load_extension(f"extension.{extension}")
        Terminal.print(f"- Loaded {extension.capitalize()}-Extension.")

    Terminal.empty()
    Terminal.print(f"Loaded {len(EXTENSIONS)} extensions!")
