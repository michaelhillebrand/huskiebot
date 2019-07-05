from PIL import Image

from commands.base import BaseCommand
from discord_bot import STATIC_PATH


class PocketSand(BaseCommand):
    trigger = 'shutup'
    description = 'HuskieBot will tell Will to shutup'
    flare_img = Image.open(STATIC_PATH + 'images/flare.png')

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
