import discord

from commands.base import BaseCommand


class Ping(BaseCommand):
    trigger = 'ping'
    description = 'HuskieBot will delete the message immediately'

    async def command(self, message):
        """
        HuskieBot will delete the message immediately

        Parameters
        ----------
        message : discord.Message

        Returns
        -------
        str
            User mention and a message

        """
        try:
            await message.delete()
        except discord.errors.Forbidden:
            await message.channel.send('I do no have the permissions to ping your message')
