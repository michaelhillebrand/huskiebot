from random import randint

import discord
from discord.ext import commands

class DiceRoll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def roll(self, ctx):
        """
        HuskieBot will roll a dice with n sides

        Parameters
        ----------
        message : discord.Message

        Returns
        -------
        int
            Random number from dice roll

        """
        args = ctx.message.content.split(' ')[1:]
        if len(args) != 1:
            await ctx.send('That is not a valid roll')
        else:
            try:
                await ctx.send(randint(1, int(args[0])))
            except ValueError:
                await ctx.send('That is not a valid roll')
