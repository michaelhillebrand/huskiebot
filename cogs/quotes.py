import random

from discord.ext import commands

from cogs.base import BaseCog


class Quotes(BaseCog):

    @commands.group(invoke_without_command=True)
    async def quote(self, ctx):
        """HuskieBot will say a quote related to its personality"""
        personality = self.bot.settings.get(self.bot.settings.CURRENT_PERSONALITY)
        quote = random.choice(personality.quotes)
        await ctx.send(quote)

    @quote.command(name='count')
    async def quote_count(self, ctx):
        """HuskieBot will say how many quotes it currently has"""
        personality = self.bot.settings.get(self.bot.settings.CURRENT_PERSONALITY)
        await ctx.send(f"I have {len(personality.quotes)} quotes")
