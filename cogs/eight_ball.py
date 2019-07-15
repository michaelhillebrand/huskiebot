import logging
from random import randint

from discord.ext import commands

from cogs.base import BaseCog


class EightBall(BaseCog):
    CHOICES = [
        'It is certain',
        'It is decidedly so',
        'Without a doubt',
        'Yes - Definitely',
        'You may rely on it',
        'As I see it, yes',
        'Most likely',
        'Outlook Good',
        'Yes',
        'Signs point to yes',
        'Reply hasy, try again',
        'Ask again later',
        'Better not tell you now',
        'Cannot predict now',
        'Concentrate and ask again',
        'Don\'t count on it',
        'My reply is no',
        'My sources say no',
        'Outlook not so good',
        'Very doubtful'
    ]

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
            await ctx.send(self.CHOICES[randint(0, len(self.CHOICES) - 1)])

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
