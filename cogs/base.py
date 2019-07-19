from discord.ext import commands


class BaseCog(commands.Cog):

    def __init__(self, bot) -> None:
        self.bot = bot
        super().__init__()
