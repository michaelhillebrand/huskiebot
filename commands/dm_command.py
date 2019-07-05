from commands.base import BaseCommand


class DMCommand(BaseCommand):
    trigger = 'dm'
    description = 'HuskieBot will tell all that the DMs word is law'

    async def command(self, message):
        """
        HuskieBot will tell all that the DMs word is law

        Parameters
        ----------
        message : discord.Message

        Returns
        -------
        str
            The DMs word is law and cannot be overruled

        """
        await message.channel.send('The DMs word is law and cannot be overruled')
