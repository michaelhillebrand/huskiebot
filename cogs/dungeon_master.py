from discord.ext import commands

from cogs.base import BaseCog


class DungeonMaster(BaseCog):

    @commands.command()
    async def dm(self, ctx: commands.Context):
        """HuskieBot will tell all that the DMs word is law"""
        await ctx.send("The DMs word is law and cannot be overruled")
