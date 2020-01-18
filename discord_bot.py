import datetime
import logging

import discord
from discord.ext import commands

from personalities.base import Personality
from personalities.bojack_horseman import BoJack
from personalities.hank_hill import Hank


class HuskieBot(commands.Bot):
    current_personality = Personality

    available_personalities = {
        'default': Personality,
        'hank': Hank,
        'bojack': BoJack
    }

    last_personality_change = datetime.datetime.utcnow()

    async def on_ready(self) -> None:
        try:
            await self.user.edit(avatar=None)
        except discord.errors.HTTPException:
            pass
        for guild in self.guilds:
            await guild.me.edit(nick=self.current_personality.name)
        logging.info('Huskie Bot Online')
