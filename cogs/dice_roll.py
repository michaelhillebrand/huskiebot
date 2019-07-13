from random import randint

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
        ctx : discord.ext.commands.Context
        sides_count : int

        Returns
        -------
        int
            Random number from dice roll
        """
        await ctx.send(randint(1, sides_count))

    @roll.error
    async def on_roll_error(self, ctx, error):
        """
        Handles error from roll command

        Parameters
        ----------
        ctx : discord.ext.commands.Context
        error : Error

        Returns
        -------
            str
        """
        await ctx.send('That is not a valid roll')
