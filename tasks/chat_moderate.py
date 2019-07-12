import logging

import discord
from discord.ext import tasks, commands


class ChatModerator(commands.Cog):
    strikes = {}

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def purge(self, ctx):
        """
        HuskieBot will clear n messages from channel

        Parameters
        ----------
        ctx : discord.ext.commands.Context

        Returns
        -------
        None

        """
        if ctx.channel.type == discord.ChannelType.private:
            await ctx.send('I can\'t purge a DM Channel')
        elif ctx.author.guild_permissions.administrator:
            try:
                args = ctx.message.content.split(' ')[1:]
                if len(args) > 1:
                    raise ValueError
                elif len(args) == 1:
                    limit = int(args[0])
                else:
                    limit = 100
                logging.info("Purging the last {limit} message from channel: {channel}".format(limit = limit, channel = ctx.channel.name))
                await ctx.channel.purge(limit=limit + 1)
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
