import logging

import discord
from discord.ext import tasks, commands


class PresenceChanger(commands.Cog):
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

    def __init__(self, bot):
        self.bot = bot
        self.index = 0
        self.presence_changer.start()

    def cog_unload(self):
        self.presence_changer.cancel()

    @tasks.loop(minutes=1)
    async def presence_changer(self):
        """
        HuskieBot will update its presence every minute with a new status from its list

        Returns
        -------
            discord.Activity
        """
        try:
            logging.info("changing presence to: type: {type}, name: {name}".format(type=self.STATUSES[self.index][0],
                                                                                   name=self.STATUSES[self.index][1]))
            await self.bot.change_presence(activity=discord.Activity(
                type=self.STATUSES[self.index][0],
                name=self.STATUSES[self.index][1]
            ))
            self.index += 1
        except IndexError:
            self.index = 0

    # TODO: Switch this to happen in a bot.event on_ready function instead
    @presence_changer.before_loop
    async def before_presence_changer(self):
        logging.info('Waiting for bot to be ready...')
        await self.bot.wait_until_ready()
