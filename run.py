"""Entry point to launch the Huskie Bot from."""

# Built-in modules
import argparse
import inspect
import logging
import os
import sys
from logging.handlers import TimedRotatingFileHandler

# Pip installed modules
import dotenv

# Local modules
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


def parse_cogs(cogs_list: str) -> list:
    """Parse the comma delineated string of cogs into a list of cog module names."""  # noqa # skip pylama "line too long"
    logging.debug(f'Parsing list of cogs to disable: {cogs_list}')
    return [*map(
        lambda cog_name:  getattr(sys.modules['cogs'], cog_name),
        cogs_list.split(',')
    )]


def parse_args() -> argparse.Namespace:
    """Define and parse command line arguments."""
    parser = argparse.ArgumentParser(description='Run the HuskieBot')

    parser.add_argument(
        '-d',
        '--disable-cogs',
        type=parse_cogs,
        help='A list of cog module names to not enable on bot startup. '
             'Comma separted list, no spaces',
        default=[]
    )

    return parser.parse_args()


def setup_bot(cogs_to_disable: list) -> HuskieBot:
    """Instantiate the bot and add default cogs."""
    logging.debug('Creating bot')
    bot_ = HuskieBot(
        command_prefix='!',
        description="HuskieBot is a collection of miscellaneous commands, "
                    "tasks, and tools used on Michael's Discord guild"
    )

    cog_classes = [
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
        SaltyBet,
        Personality,
        Deepfry
    ]

    logging.debug('Adding cogs to bot')
    for cog_class in cog_classes:
        if not inspect.getmodule(cog_class) in cogs_to_disable:
            logging.debug(f'Enabling cog {cog_class}')
            bot_.add_cog(cog_class(bot=bot_))
        else:
            logging.debug(f"Skipping cog {cog_class}")
    return bot_


if __name__ == '__main__':
    dotenv.load_dotenv()
    handler = TimedRotatingFileHandler(
        filename='logs/bot.log',
        when='midnight',
        backupCount=30,
        utc=True
    )
    logging.basicConfig(
        level=logging.DEBUG if os.environ['ENVIRONMENT'] == 'development' else logging.INFO,  # noqa # skip pylama "line too long"
        format='[%(asctime)s] [%(levelname)s] [%(module)s] %(message)s',
        handlers=[handler]
    )

    args = parse_args()
    logging.debug(f'Args passed from commandline: {args}')

    bot = setup_bot(args.disable_cogs)
    bot.run(os.getenv('DISCORD_BOT_TOKEN'))
