import datetime
import random
from io import BytesIO
from os.path import join

from discord.ext import commands

from cogs import IMAGES_PATH
from cogs.base import BaseCog


class Personality(BaseCog):

    @commands.command()
    async def change_personality(self, ctx: commands.Context, personality_slug: str) -> None:
        """
        HuskieBot will change to another personality

        Parameters
        ----------
        ctx : discord.ext.commands.Context
        personality_slug: str

        Returns
        -------
        None
        """
        now = datetime.datetime.utcnow()
        settings = self.bot.settings
        last_personality_change = settings.get(settings.LAST_PERSONALITY_CHANGE)
        # Check if the bot has been changed within the last 2 minutes
        if last_personality_change and (last_personality_change + datetime.timedelta(minutes=2)) > now:
            raise RuntimeError('Changed personalities too soon')
        personality = self.bot.available_personalities.get(personality_slug.lower())
        if not personality:
            await ctx.send('That is not a valid personality')
            return
        settings.update({
            settings.CURRENT_PERSONALITY: personality,
            settings.LAST_PERSONALITY_CHANGE: now
        })
        await ctx.me.edit(nick=personality.name)
        if personality.avatar_path:
            with open(join(IMAGES_PATH, personality.avatar_path), 'rb') as file:
                avatar = BytesIO(file.read())
                await self.bot.user.edit(avatar=avatar.read())
        await ctx.send(random.choice(personality.greetings))

    @change_personality.error
    async def on_change_personality_error(self, ctx: commands.Context, error: commands.CommandInvokeError) -> None:
        """
        Handles error from change personality command

        Parameters
        ----------
        ctx : discord.ext.commands.Context
        error : discord.ext.commands.CommandInvokeError

        Returns
        -------
        None
        """
        await ctx.send(error.original.__str__())
