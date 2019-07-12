import logging
import typing

import discord
from discord.ext import tasks, commands


class ChatModerator(commands.Cog):
    strikes = {}

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def purge(self, ctx, purge_limit: typing.Optional[int] = 5):
        """
        HuskieBot will clear n messages from channel

        Parameters
        ----------
        ctx : discord.ext.commands.Context

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

                logging.info("Purging the purge command and the last {limit} message(s) from channel: {channel}".format(limit = purge_limit, channel = ctx.channel.name))
                await ctx.channel.purge(limit=purge_limit + 1)
            except ValueError:
                await ctx.send('That is not a valid number')
            except discord.errors.Forbidden:
                await ctx.send('I do no have the permissions to do that')
        else:
            await ctx.send('You do no have the permissions to do that')

    @commands.command()
    async def chat_moderate(self, ctx):
        """(NOT IMPLEMENTED YET) Enable or disable chat moderation"""
        pass
