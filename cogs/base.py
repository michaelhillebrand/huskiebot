import logging

from discord.ext import commands


class BaseCog(commands.Cog):

    def __init__(self, bot) -> None:
        self.bot = bot
        super().__init__()

    async def cog_before_invoke(self, ctx: commands.Context) -> None:
        logging.debug(f'{ctx.author} invoked command {ctx.command} with message {ctx.message.content}')
