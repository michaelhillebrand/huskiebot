import logging
import os
from logging.handlers import TimedRotatingFileHandler

import dotenv

from cogs.chat_moderate import ChatModerator
from cogs.dank_memes import DankMemes
from cogs.deepfry import Deepfry
from cogs.dice_roll import DiceRoll
from cogs.dungeon_master import DungeonMaster
from cogs.eight_ball import EightBall
from cogs.example import Example
from cogs.personality import Personality
from cogs.ping import Ping
from cogs.presence_changer import PresenceChanger
from cogs.quotes import Quotes
from cogs.rps import RockPaperScissors
from cogs.salty_bet import SaltyBet
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
        # GruNosePoster
        SaltyBet,
        Personality,
        SaltyBet,
        Deepfry
    ]
    for cog in cogs:
        bot_.add_cog(cog(bot=bot_))
    return bot_


if __name__ == '__main__':
    dotenv.load_dotenv()
    handler = TimedRotatingFileHandler(filename='logs/bot.log', when='midnight', backupCount=30, utc=True)
    logging.basicConfig(level=logging.DEBUG if os.environ['ENVIRONMENT'] == 'development' else logging.INFO,
                        format='[%(asctime)s] [%(levelname)s] [%(module)s] %(message)s',
                        handlers=[handler])

    bot = setup_bot()
    bot.run(os.getenv('DISCORD_BOT_TOKEN'))
