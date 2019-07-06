import os
import random
from discord_webhook import DiscordWebhook, DiscordEmbed
import asyncio
from tasks.base import BaseTask


class DaleAttack(BaseTask):
    """

    When running, Dale Gibble randomly attacks with the person on thier turn, player or not

    :param: None
    :return: Embeded Discord Webhook
    """

    id = 'dale-attack'
    channel = None

    async def task(self):
        webhook = DiscordWebhook(
            url='https://discordapp.com/api/webhooks/596806839136419859/QtKJScaEKMfaTs2SMJVpBtuR610RtQVIUtunfgzzq3QBPw91-bLfry37lgKAlC710svS')
        pocket_sand_url = 'https://i.kym-cdn.com/photos/images/original/001/295/678/f81.png'

        if not self.channel:
            self.channel = self.client.get_channel(os.getenv('POCKET_SAND_TOKEN'))
        while True:
            attack_time = random.randint(3, 6)
            await asyncio.sleep(attack_time)
            embed = DiscordEmbed(title='POCKETSAND FOR +2 ATTACK')
            embed.set_image(url=pocket_sand_url)
            webhook.add_embed(embed)
            webhook.execute()
