import asyncio
import datetime

import discord

from tasks.base import BaseTask


class GruNosePoster(BaseTask):
    id = 'gru-nose'
    channel = None

    async def task(self):
        if not self.channel:
            self.channel = self.client.get_channel(537442178289500160)
        while True:
            now = datetime.datetime.now()
            if now.hour == 20:
                print("It's 8:00pm!")  # TODO add to log
                try:
                    await self.channel.send(file=discord.File(self.client.base_path, 'gru/{}.png'.format(now.date())))
                except FileNotFoundError:
                    pass  # TODO log failure
            await asyncio.sleep(3600)  # check every hour
