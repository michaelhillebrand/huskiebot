import asyncio
import datetime
import logging
import os

import discord
from discord.ext import tasks, commands

from discord_bot import BASE_PATH

class GruNosePoster(commands.Cog):
    channel_id = 594707074609577994

    def __init__(self, bot):
        self.bot = bot
        self.gru_nose_poster.start()

    def cog_unload(self):
        self.gru_nose_poster.cancel()

    @tasks.loop(hours=1.0)
    async def gru_nose_poster(self):
        channel = self.bot.get_channel(self.channel_id)
        now = datetime.datetime.now()
        if now.hour == 20:
            print("It's 8:00pm!")  # TODO add to log
            try:
                await channel.send(file=discord.File(os.path.join(BASE_PATH, 'gru/{}.png'.format(now.date()))))
            except FileNotFoundError:
                pass  # TODO log failure

    @gru_nose_poster.before_loop
    async def before_gru_nose_poster(self):
        logging.info('Waiting for bot to be ready...')
        await self.bot.wait_until_ready()
