import discord
from discord import FFmpegPCMAudio

from commands.base import BaseCommand


class InviteBot(BaseCommand):
    trigger = 'invitebot'
    description = 'Invite HuskieBot to user\'s voice channel'

    def get_current_voice_client(self, message):
        for vc in self.client.voice_clients:
            if vc.guild == message.guild:
                return vc
        return None

    async def command(self, message):
        """
        HuskieBot will join user's voice channel

        Parameters
        ----------
        message : discord.Message

        Returns
        -------
        None

        """
        vc = self.get_current_voice_client(message)
        if vc:
            await vc.move_to(message.author.voice.channel)
        else:
            vc = await message.author.voice.channel.connect()
        # vc.play(FFmpegPCMAudio('/home/michael/i_am_here.mp3'))


class DisconnectBot(BaseCommand):
    trigger = 'disconnectbot'
    description = 'Invite HuskieBot to user\'s voice channel'

    def get_current_voice_client(self, message):
        for vc in self.client.voice_clients:
            if vc.guild == message.guild:
                return vc
        return None

    async def command(self, message):
        """
        HuskieBot will disconnect from its voice channel

        Parameters
        ----------
        message : discord.Message

        Returns
        -------
        None

        """
        vc = self.get_current_voice_client(message)
        if not vc:
            await message.channel.send('HuskieBot is not in a voice channel')
        else:
            await vc.disconnect()
