# Standard library
import logging
import os

# Pip installed libraries
import dotenv

# Local libraries
from cogs.example import Example
from cogs.dungeonmaster import DungeonMaster
from cogs.quotes import Quotes
from commands.dank_meme_poster import DankMemePoster
from commands.dice_roll import DiceRoll
from commands.eight_ball import EightBall
from commands.invite_bot import InviteBot, DisconnectBot
from commands.ping import Ping
from commands.rps import RockPaperScissors
from commands.shutup_will import ShutupWill
from discord_bot import HuskieBot, HuskieBotCogs
from tasks.chat_moderate import ChatModerator
from tasks.gru_nose import GruNosePoster
from tasks.presence_changer import PresenceChanger

def useCogs(DISCORD_BOT_TOKEN):
    bot = HuskieBotCogs(
        command_prefix='!',
        description="test bot"
    )

    cogs = [
        Example,
        DungeonMaster,
        Quotes
    ]

    for cog in cogs:
        bot.add_cog(cog(bot))

    bot.run(DISCORD_BOT_TOKEN)

def useOriginal(DISCORD_BOT_TOKEN):
    client = HuskieBot(commands=[
        EightBall,
        DiceRoll,
        ShutupWill,
        RockPaperScissors,
        DankMemePoster,
        InviteBot,
        DisconnectBot,
        Ping,
    ], tasks=[
        GruNosePoster,
        ChatModerator,
        PresenceChanger,
    ])
    client.run(DISCORD_BOT_TOKEN)

if __name__ == '__main__':
    # Config
    logging.basicConfig(level=logging.INFO)
    dotenv.load_dotenv()
    DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')

    useCogs(DISCORD_BOT_TOKEN)
    # useOriginal(DISCORD_BOT_TOKEN)
