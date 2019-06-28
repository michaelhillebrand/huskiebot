from commands.base import BaseCommand


class InviteBot(BaseCommand):
    trigger = 'invitebot'
    description = 'Invite HuskieBot to user\'s voice channel'

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
        await message.author.voice.channel.connect()