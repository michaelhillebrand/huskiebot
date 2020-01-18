import logging

import discord
from discord.ext import tasks

from cogs.base import BaseCog


class PresenceChanger(BaseCog):
    """
    from discord.enums:
    class ActivityType(Enum):
        unknown = -1
        playing = 0
        streaming = 1
        listening = 2
        watching = 3
    """

    def __init__(self, bot) -> None:
        self.index = 0
        self.presence_changer.start()
        super().__init__(bot)

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
            logging.info("changing presence to: type: {type}, name: {name}".format(type=self.bot.current_personality.presence_options[self.index][0],
                                                                                   name=self.bot.current_personality.presence_options[self.index][1]))
            await self.bot.change_presence(activity=discord.Activity(
                type=self.bot.current_personality.presence_options[self.index][0],
                name=self.bot.current_personality.presence_options[self.index][1]
            ))
            self.index += 1
        except IndexError:
            self.index = 0

    @presence_changer.before_loop
    async def before_presence_changer(self):
        await self.bot.wait_until_ready()
