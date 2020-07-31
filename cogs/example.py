import random

import discord
from discord.ext import commands

from cogs.base import BaseCog


class Example(BaseCog):
    _last_member = None

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
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
            personality = self.bot.settings.get('current_personality')
            greeting = random.choice(personality.member_greetings)
            await channel.send(greeting.format(member.mention))

    @commands.command(hidden=True)
    async def hello(self, ctx: commands.Context, *, member: discord.Member = None):
        """Says hello"""
        member = member or ctx.author
        if self._last_member is None or self._last_member.id != member.id:
            await ctx.send(f'Hello {member.name}')
        else:
            await ctx.send(f'Hello {member.name}... This feels familiar.')
        self._last_member = member

    @commands.group(hidden=True)
    async def cool(self, ctx: commands.Context):
        """Says if a user is cool.
        In reality this just checks if a subcommand is being invoked.
        """
        if ctx.invoked_subcommand is None:
            await ctx.send(f'No, {ctx.subcommand_passed} is not cool')

    @cool.command(name='bot')
    async def _bot(self, ctx: commands.Context):
        """Is the bot cool?"""
        await ctx.send('Yes, the bot is cool.')

    @commands.command(hidden=True)
    async def tick(self, ctx: commands.Context):
        """Responds with "tock" to prove that commands work"""
        await ctx.send('tock')
