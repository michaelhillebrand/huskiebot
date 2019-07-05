from commands.base import BaseCommand
from discord_webhook import DiscordWebhook, DiscordEmbed


class PocketSand(BaseCommand):
    trigger = 'ps'
    description = 'pocket sand'

    async def command(self, message):
        """
        Command to let all know that the DM is god

        :param message: discord.Message
        :return str:
        """
        webhook = DiscordWebhook(url='https://discordapp.com/api/webhooks/596806839136419859/QtKJScaEKMfaTs2SMJVpBtuR610RtQVIUtunfgzzq3QBPw91-bLfry37lgKAlC710svS')

        # create embed object for webhook
        embed = DiscordEmbed(title='Dale Gribble', description='Lorem ipsum dolor sit', color=242424)

        # add embed object to webhook
        webhook.add_embed(embed)

        webhook.execute()
