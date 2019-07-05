import random
from discord_bot import STATIC_PATH
import asyncio
import os
import discord
from tasks.base import BaseTask


class DaleAttack(BaseTask):
    id = 'dale-attack'
    channel = None

    async def task(self):
        if not self.channel:
            self.channel = self.client.get_channel(596772352835190823)
        while True:
            attack_time = random.randint(300, 600)
            await asyncio.sleep(attack_time)
            await self.channel.send('POCKET SAND FOR +2 ATTACK', file=discord.File(os.path.join(STATIC_PATH, 'images/pocket_sand.jpg')))

