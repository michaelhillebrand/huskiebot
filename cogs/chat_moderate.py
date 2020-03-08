import logging
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
            logging.info(f'{ctx.author} tried to purge a DM channel')
            await ctx.send('I can\'t purge a DM Channel')
        elif ctx.author.guild_permissions.administrator:
            try:
                if purge_limit < min_purge_limit:
                    raise ValueError
                logging.info(f"Purging the last {purge_limit} message(s) from channel: {ctx.channel.name}")
                await ctx.channel.purge(limit=purge_limit + 1)
            except ValueError:
                logging.warning(f'{ctx.author} failed to purge a channel with a purge limit of {purge_limit}')
                await ctx.send('That is not a valid number')
        else:
            logging.warning(f'{ctx.author} failed to purge a channel')
            await ctx.send('You do no have the permissions to do that')

    @commands.command()
    async def chat_moderate(self, ctx):
        """(NOT IMPLEMENTED YET) Enable or disable chat moderation"""
        pass
