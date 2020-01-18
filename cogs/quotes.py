import random
import typing

from discord.ext import commands

from cogs.base import BaseCog


class Quotes(BaseCog):

    @commands.group(invoke_without_command=True)
    async def quote(self, ctx):
        """HuskieBot will say a quote related to its personality"""
        await ctx.send(random.choice(self.bot.current_personality.quotes))

    @quote.command(name='count')
    async def quote_count(self, ctx):
        """HuskieBot will say how many quotes it currently has"""
        await ctx.send(f"I have {len(self.bot.current_personality.quotes)} quotes")
