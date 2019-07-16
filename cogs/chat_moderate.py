import logging
import random
import typing

import discord
from discord.ext import commands

from cogs.base import BaseCog


class ChatModerator(BaseCog, command_attrs={'hidden': True}):
    strikes = {}

    @commands.command()
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
        min_purge_limit = 1
        if ctx.channel.type == discord.ChannelType.private:
            await ctx.send('I can\'t purge a DM Channel')
        elif ctx.author.guild_permissions.administrator:
            try:
                if purge_limit < min_purge_limit:
                    raise ValueError
                logging.info("Purging the last {limit} message(s) "
                             "from channel: {channel}".format(limit=purge_limit, channel=ctx.channel.name))
                await ctx.channel.purge(limit=purge_limit + 1)
            except ValueError:
                await ctx.send('That is not a valid number')
        else:
            await ctx.send('You do no have the permissions to do that')

    @commands.command()
    async def chat_moderate(self, ctx):
        """(NOT IMPLEMENTED YET) Enable or disable chat moderation"""
        pass

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        """(NOT IMPLEMENTED YET) Enable or disable chat moderation"""
        if before.content != after.content and random.random() <= .1:
            await after.channel.send('I saw you change that {}'.format(after.author.mention))

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        """(NOT IMPLEMENTED YET) Enable or disable chat moderation"""
        if before.nick != after.nick and after.guild.system_channel is not None:
            await after.guild.system_channel.send('{} is now called {}'.format(before.name,
                                                                               after.nick if after.nick
                                                                               else after.name))

    @commands.Cog.listener()
    async def on_guild_channel_pins_update(self, channel, last_pin):
        """(NOT IMPLEMENTED YET) Enable or disable chat moderation"""
        await channel.send('Another fine pin for the great state of Texas')

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
