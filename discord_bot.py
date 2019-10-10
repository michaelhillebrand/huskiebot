import logging

from discord.ext import commands
from discord.ext.commands import Cog


class HuskieBot(commands.Bot):

    async def on_ready(self):
        logging.info('Huskie Bot Online')

    async def on_command_error(self, context, exception):
        if self.extra_events.get('on_command_error', None):
            return

        if hasattr(context.command, 'on_error'):
            return

        cog = context.cog
        if cog:
            if Cog._get_overridden_method(cog.cog_command_error) is not None:
                return

        await context.channel.send('That is not a valid command')
