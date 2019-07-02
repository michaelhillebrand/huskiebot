import asyncio
import datetime
import logging
import os

import discord

from discord_bot import BASE_PATH
from tasks.base import BaseTask


class GruNosePoster(BaseTask):
    id = 'gru-nose'
    channel = None

    async def task(self):
        if not self.channel:
            self.channel = self.client.get_channel(594707074609577994)
        while True:
            now = datetime.datetime.now()
            if now.hour == 20:
                try:
                    await self.channel.send(file=discord.File(os.path.join(BASE_PATH, 'ygru/{}.png'.format(now.date()))))
                except FileNotFoundError as e:
                    logging.error("Failed to post Gru nose picture: {}".format(e))
            await asyncio.sleep(3600)  # check every hour
