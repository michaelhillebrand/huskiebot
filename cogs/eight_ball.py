from random import randint

import discord
from discord.ext import commands

class EightBall(commands.Cog):
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

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["8ball"])
    async def eight_ball(self, ctx, question: str):
        """
        User asks the bot a question and returns an answer

        Parameters
        ----------
        message : discord.Message
            A question to answer (Must end with "?")

        Returns
        -------
        str
            A randomly selected answer

        """

        if question[-1] != '?':
            await ctx.send('You need to ask a question')
        else:
            await ctx.send(self.CHOICES[randint(0, len(self.CHOICES) - 1)])

    @eight_ball.error
    async def on_eight_ball_error(self, ctx, error):
        await ctx.send('You need to ask a question')
