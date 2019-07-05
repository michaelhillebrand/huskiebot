from random import randint

from commands.base import BaseCommand


class DiceRoll(BaseCommand):
    trigger = 'roll'
    description = 'Roll a die with n sides'

    async def command(self, message):
        """
        HuskieBot will roll a dice with n sides

        Parameters
        ----------
        message : discord.Message

        Returns
        -------
        int
            Random number from dice roll

        """
        args = message.content.split(' ')[1:]
        if len(args) != 1:
            await message.channel.send('That is not a valid roll')
        else:
            try:
                await message.channel.send(randint(1, int(args[0])))
            except ValueError:
                await message.channel.send('That is not a valid roll')
