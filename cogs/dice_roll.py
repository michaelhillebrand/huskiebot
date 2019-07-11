from random import randint

import discord
from discord.ext import commands

class DiceRoll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def roll(self, ctx, sides_count: int):
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
        await ctx.send(randint(1, sides_count))

    @roll.error
    async def on_roll_error(self, ctx, error):
        await ctx.send('That is not a valid roll')
