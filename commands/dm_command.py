from commands.base import BaseCommand


class DMCommand(BaseCommand):
    trigger = 'dm'
    description = 'HuskieBot will tell all that the DMs word is law'

    async def command(self, message):
        """
        Command to let all know that the DM is god

        :param message: discord.Message
        :return str:
        """
        await message.channel.send('The DMs word is law and cannot be overruled')
