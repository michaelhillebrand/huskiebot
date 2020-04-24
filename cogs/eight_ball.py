import logging
import random

from discord.ext import commands

from cogs.base import BaseCog


class EightBall(BaseCog):

    @commands.command(aliases=["8ball"])
    async def eight_ball(self, ctx, *, arg):
        """
        User asks the bot a question and returns an answer

        Parameters
        ----------
        ctx : discord.ext.commands.Context
        arg : str (question)

        Returns
        -------
        str
            A randomly selected answer
        """
        if arg[-1] != '?':
            await ctx.send('You need to ask a question')
        else:
            choices = self.bot.settings.get('current_personality').eight_ball_responses
            await ctx.send(random.choice(choices))

    @eight_ball.error
    async def on_eight_ball_error(self, ctx, error):
        """
        Handles error for eight_ball command

        Parameters
        ----------
        ctx : discord.ext.commands.Context
        error : Error

        Returns
        -------
        str
        """
        logging.error(error)
        await ctx.send('You need to ask a question')
