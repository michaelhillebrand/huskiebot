import logging

from discord.ext import commands


class HuskieBot(commands.Bot):

    async def on_ready(self):
        logging.info('Huskie Bot Online')
