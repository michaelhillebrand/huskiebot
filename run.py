# Standard library
import logging
import os

# Pip installed libraries
import dotenv

# Local libraries
from cogs.chat_moderate import ChatModerator
from cogs.dice_roll import DiceRoll
from cogs.dungeonmaster import DungeonMaster
from cogs.eight_ball import EightBall
from cogs.example import Example
from cogs.gru_nose import GruNosePoster
from cogs.ping import Ping
from cogs.presence_changer import PresenceChanger
from cogs.quotes import Quotes
from cogs.rps import RockPaperScissors
from cogs.shutup_will import ShutupWill
from cogs.voice import Voice
from cogs.dank_memes import DankMemes
from discord_bot import HuskieBot, HuskieBotCogs

def useCogs(DISCORD_BOT_TOKEN):
    bot = HuskieBotCogs(
        command_prefix='!',
        description="test bot"
    )

    cogs = [
        Example,
        DungeonMaster,
        Quotes,
        ShutupWill,
        Ping,
        EightBall,
        DiceRoll,
        RockPaperScissors,
        Voice,
        DankMemes,
        PresenceChanger,
        ChatModerator,
        GruNosePoster
    ]

    for cog in cogs:
        bot.add_cog(cog(bot))

    bot.run(DISCORD_BOT_TOKEN)

def useOriginal(DISCORD_BOT_TOKEN):
    client = HuskieBot(commands=[], tasks=[])
    client.run(DISCORD_BOT_TOKEN)

if __name__ == '__main__':
    # Config
    logging.basicConfig(level=logging.INFO)
    dotenv.load_dotenv()
    DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')

    useCogs(DISCORD_BOT_TOKEN)
    # useOriginal(DISCORD_BOT_TOKEN)
