import datetime
from io import BytesIO
from os.path import join

from discord.ext import commands

from cogs import IMAGES_PATH
from cogs.base import BaseCog


class Personality(BaseCog):

    @commands.command()
    async def change_personality(self, ctx, personality: str) -> None:
        """HuskieBot will change to another personality

        Parameters
        ----------
        ctx : discord.ext.commands.Context
        personality: str

        Returns
        -------
        None
        """
        if (self.bot.last_personality_change + datetime.timedelta(minutes=10)) > datetime.datetime.utcnow():
            raise RuntimeError('Changed personalities too soon')
        try:
            self.bot.current_personality = self.bot.available_personalities[personality.lower()]
        except KeyError:
            await ctx.send('That is not a valid personality')
            return
        await ctx.me.edit(nick=self.bot.current_personality.name)
        if self.bot.current_personality.avatar_path:
            with open(join(IMAGES_PATH, self.bot.current_personality.avatar_path), 'rb') as file:
                avatar = BytesIO(file.read())
                await self.bot.user.edit(avatar=avatar.read())
        await ctx.send(self.bot.current_personality.greetings[0])

    @change_personality.error
    async def on_change_personality_error(self, ctx, error):
        """Handles error from change personality command

        Parameters
        ----------
        ctx : discord.ext.commands.Context
        error : Error

        Returns
        -------
            str
        """
        await ctx.send(error)
