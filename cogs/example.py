import discord
from discord.ext import commands

from cogs.base import BaseCog


class Example(BaseCog):

    def __init__(self, bot) -> None:
        self._last_member = None
        super().__init__(bot)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        """
        HuskieBot will welcome new users to the server

        Parameters
        ----------
        member : discord.Member

        Returns
        -------
        str
            HuskieBot's greeting
        """
        channel = member.guild.system_channel
        if channel is not None:
            await channel.send('Welcome {0.mention}.'.format(member))

    @commands.command(hidden=True)
    async def hello(self, ctx, *, member: discord.Member = None):
        """Says hello"""
        member = member or ctx.author
        if self._last_member is None or self._last_member.id != member.id:
            await ctx.send('Hello {0.name}'.format(member))
        else:
            await ctx.send('Hello {0.name}... This feels familiar.'.format(member))
        self._last_member = member

    @commands.group(hidden=True)
    async def cool(self, ctx):
        """Says if a user is cool.
        In reality this just checks if a subcommand is being invoked.
        """
        if ctx.invoked_subcommand is None:
            await ctx.send('No, {0.subcommand_passed} is not cool'.format(ctx))

    @cool.command(name='bot')
    async def _bot(self, ctx):
        """Is the bot cool?"""
        await ctx.send('Yes, the bot is cool.')

    @commands.command(hidden=True)
    async def tick(self, ctx):
        """Responds with "tock" to prove that commands work"""
        await ctx.send('tock')
