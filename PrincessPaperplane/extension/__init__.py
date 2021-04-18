from discord.ext.commands import Bot

HTTP_CODES = {
    200: "All right!",
    401: "You fucked up!",
    418: "I'm a teapot!",
    429: "Too many requests!"
}


def load_extensions(bot: Bot):
    bot.load_extension("extension.dice")
    bot.load_extension("extension.quotes")
