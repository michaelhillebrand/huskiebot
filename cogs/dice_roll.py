import logging
import re
from random import randint

from discord.ext import commands

from cogs.base import BaseCog

DICE_REGEX = re.compile(r"^(?P<rolls>\d+)d(?P<type>\d+)$")


class DiceRoll(BaseCog):

    @commands.command()
    async def roll(self, ctx: commands.Context, sides_count: str):
        """
        HuskieBot will roll a dice with n sides.

        Parameters
        ----------
        ctx : discord.ext.commands.Context
        sides_count : int

        Returns
        -------
        int
            Random number from dice roll
        """
        match = DICE_REGEX.match(sides_count)
        if match:
            rolls, dice_type = match.groups()
            rolls = int(rolls)
            await ctx.send(randint(rolls, rolls * int(dice_type)))
        else:
            await ctx.send(randint(1, int(sides_count)))

    @roll.error
    async def on_roll_error(self, ctx: commands.Context, error: commands.CommandInvokeError):
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
        logging.error(error)
        await ctx.send('That is not a valid roll')
