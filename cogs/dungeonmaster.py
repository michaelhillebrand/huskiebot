import discord
from discord.ext import commands

class DungeonMaster(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def dm(self, ctx):
        """HuskieBot will tell all that the DMs word is law"""
        await ctx.send("The DMs word is law and cannot be overruled, I tell you h'what")
