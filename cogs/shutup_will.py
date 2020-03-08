from discord.ext import commands

from cogs.base import BaseCog


class ShutupWill(BaseCog):
    will = None

    @commands.command()
    async def shutup(self, ctx):
        """
        HuskieBot tells Will to shutup

        Parameters
        ----------
        ctx : discord.ext.commands.Context

        Returns
        -------
        str
            Will's User mention
        """
        if not self.will:
            self.will = ctx.bot.get_user(187364654455062528)
        await ctx.send(f'{self.will.mention} Shut up!')
