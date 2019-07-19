import logging
import os

import dotenv

from cogs.chat_moderate import ChatModerator
from cogs.dank_memes import DankMemes
from cogs.dice_roll import DiceRoll
from cogs.dungeon_master import DungeonMaster
from cogs.eight_ball import EightBall
from cogs.example import Example
from cogs.gru_nose import GruNosePoster
from cogs.ping import Ping
from cogs.presence_changer import PresenceChanger
from cogs.quotes import Quotes
from cogs.rps import RockPaperScissors
from cogs.shutup_will import ShutupWill
from cogs.voice import Voice
from discord_bot import HuskieBot


def setup_bot():
    bot_ = HuskieBot(
        command_prefix='!',
        description="HuskieBot is a collection of miscellaneous commands, "
                    "tasks, and tools used on Michael's Discord guild"
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
        bot_.add_cog(cog(bot=bot_))
    return bot_


if __name__ == '__main__':
    # Config
    logging.basicConfig(level=logging.INFO)
    dotenv.load_dotenv()

    bot = setup_bot()
    bot.run(os.getenv('DISCORD_BOT_TOKEN'))
