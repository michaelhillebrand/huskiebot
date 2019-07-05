from commands.base import BaseCommand


class ShutupWill(BaseCommand):
    trigger = 'shutup'
    description = 'HuskieBot will tell Will to shutup'

    will = None

    async def command(self, message):
        """
        HuskieBot tells Will to shutup

        Parameters
        ----------
        message : discord.Message

        Returns
        -------
        str
            Will's User mention

        """
        if not self.will:
            self.will = self.client.get_user(187364654455062528)
        await message.channel.send('{} Shut up!'.format(self.will.mention))
