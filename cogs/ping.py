import discord
from discord.ext import commands

class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        """
        HuskieBot will delete the message immediately

        Parameters
        ----------
        message : discord.Message

        Returns
        -------
        str
            User mention and a message

        """
        try:
            await ctx.message.delete()
        except discord.errors.Forbidden:
            await ctx.send('I do no have the permissions to ping your message')
