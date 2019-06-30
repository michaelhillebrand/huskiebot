import asyncio

import discord

from tasks.base import BaseTask


class PresenceChanger(BaseTask):
    id = 'presence-changer'

    STATUSES = [
        (0, 'shitposting memes'),
        (0, 'Tuber Simulator'),
        (2, 'the developers'),
        (3, 'dank memes'),
        (0, 'Uploading dank memes'),
        (3, 'sad horse show'),
        (0, 'the game'),
        (0, 'Dungons and Drags'),
        (3, 'the world burn'),
    ]

    """
    from discord.enums:
    class ActivityType(Enum):
        unknown = -1
        playing = 0
        streaming = 1
        listening = 2
        watching = 3
    """

    async def task(self):
        i = 0
        while True:
            try:
                await self.client.change_presence(activity=discord.Activity(
                    type=self.STATUSES[i][0],
                    name=self.STATUSES[i][1]
                ))
                i += 1
                await asyncio.sleep(60)
            except IndexError:
                i = 0
