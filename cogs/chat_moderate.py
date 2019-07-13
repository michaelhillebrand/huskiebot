import logging
import typing

import discord
from discord.ext import commands

from cogs.base import BaseCog


class ChatModerator(BaseCog):
    strikes = {}

    @commands.command(hidden=True)
    async def purge(self, ctx, purge_limit: typing.Optional[int] = 100):
        """
        HuskieBot will clear n messages from channel

        Parameters
        ----------
        ctx : discord.ext.commands.Context
        purge_limit : int

        Returns
        -------
        None

        """
        if ctx.channel.type == discord.ChannelType.private:
            await ctx.send('I can\'t purge a DM Channel')
        elif ctx.author.guild_permissions.administrator:
            try:
                if purge_limit < 1:
                    raise ValueError
                logging.info("Purging the last {limit} message(s) "
                             "from channel: {channel}".format(limit=purge_limit, channel=ctx.channel.name))
                await ctx.channel.purge(limit=purge_limit + 1)
            except ValueError:
                await ctx.send('That is not a valid number')
            except discord.errors.Forbidden:
                await ctx.send('I do no have the permissions to do that')
        else:
            await ctx.send('You do no have the permissions to do that')

    @commands.command(hidden=True)
    async def chat_moderate(self, ctx):
        """(NOT IMPLEMENTED YET) Enable or disable chat moderation"""
        pass
