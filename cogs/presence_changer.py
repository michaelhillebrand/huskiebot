import logging

import discord
from discord.ext import tasks

from cogs.base import BaseCog


class PresenceChanger(BaseCog):

    def __init__(self, bot) -> None:
        self.index = 0
        self.presence_changer.start()
        super().__init__(bot)

    def cog_unload(self):
        self.presence_changer.cancel()

    @tasks.loop(minutes=1)
    async def presence_changer(self):
        """HuskieBot will update its presence every minute with a new status from its list

        Returns
        -------
            discord.Activity
        """
        personality = self.bot.settings.get(self.bot.settings.CURRENT_PERSONALITY)
        if self.index + 1 >= len(personality.presence_options):
            self.index = 0
        presence = personality.presence_options[self.index]
        logging.debug(f"changing presence to: type: {presence[0]}, name: {presence[1]}")
        await self.bot.change_presence(activity=discord.Activity(
            type=presence[0],
            name=presence[1]
        ))
        self.index += 1

    @presence_changer.before_loop
    async def before_presence_changer(self):
        await self.bot.wait_until_ready()
