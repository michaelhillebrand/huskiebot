import discord
from discord.ext import commands

class ShutupWill(commands.Cog):
    will = None
    
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def shutup(self, ctx):
        """
        HuskieBot tells Will to shutup

        Parameters
        ----------
        message : discord.Message

        Returns
        -------
        str
            Will's User mention

        """
        if not self.will:
            self.will = ctx.bot.get_user(187364654455062528)
        await ctx.send('{} Shut up!'.format(self.will.mention))
