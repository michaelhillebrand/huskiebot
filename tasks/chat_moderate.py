import discord

from commands.base import BaseCommand
from tasks.base import BaseTask


class PurgeChat(BaseCommand):
    trigger = 'purge'
    description = 'HuskieBot will clear n messages from channel'

    async def command(self, message):
        """
        HuskieBot will clear n messages from channel

        Parameters
        ----------
        message : discord.Message

        Returns
        -------
        None

        """
        if message.channel.type == discord.ChannelType.private:
            await message.channel.send('I can\'t purge a DM Channel')
        elif message.author.guild_permissions.administrator:
            try:
                args = message.content.split(' ')[1:]
                if len(args) > 1:
                    raise ValueError
                elif len(args) == 1:
                    limit = int(args[0])
                else:
                    limit = 100
                await message.channel.purge(limit=limit + 1)
            except ValueError:
                await message.channel.send('That is not a valid number')
            except discord.errors.Forbidden:
                await message.channel.send('I do no have the permissions to do that')
        else:
            await message.channel.send('You do no have the permissions to do that')


class ChatModerator(BaseTask):
    id = 'chat-moderator'
    strikes = {}

    async def before_task(self):
        await self.client.add_commands([
            PurgeChat
        ])

    async def task(self):
        pass
