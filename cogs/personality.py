import datetime
import logging
import random
from io import BytesIO
from os.path import join

from discord.ext import commands

from cogs import IMAGES_PATH
from cogs.base import BaseCog


class Personality(BaseCog):

    @commands.command(aliases=["personalities"])
    async def list_personalities(self, ctx: commands.Context):
        """ HuskieBot will list available personalities to change to."""
        personality_list = '\n'.join(f'{personality.name} ({personality.slug})' for _, personality
                                     in self.bot.available_personalities.items())
        await ctx.send(personality_list)

    @commands.command()
    async def change_personality(self, ctx: commands.Context, personality_slug: str):
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
        # Check if the bot has been changed within the last 5 minutes
        if last_personality_change and (last_personality_change + datetime.timedelta(minutes=5)) > now:
            raise RuntimeError("I just changed my personality, I can't do it again so soon")
        personality = self.bot.available_personalities.get(personality_slug.lower())
        if not personality:
            await ctx.send('That is not a valid personality')
            return
        if personality.avatar_path:
            with open(join(IMAGES_PATH, personality.avatar_path), 'rb') as file:
                avatar = BytesIO(file.read())
                await self.bot.user.edit(avatar=avatar.read())
        await ctx.me.edit(nick=personality.name)
        settings.update({
            settings.CURRENT_PERSONALITY: personality,
            settings.LAST_PERSONALITY_CHANGE: now
        })
        await ctx.send(random.choice(personality.greetings))

    @change_personality.error
    async def on_change_personality_error(self, ctx: commands.Context, error: commands.CommandInvokeError):
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
        logging.error(error)
        await ctx.send("I can't change personalities right now")
