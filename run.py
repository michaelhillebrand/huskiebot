# Standard library
import logging
import os

# Pip installed libraries
import dotenv

# Local libraries
from commands.dank_meme_poster import DankMemePoster
from commands.dice_roll import DiceRoll
from commands.dm_command import DMCommand
from commands.eight_ball import EightBall
from commands.invite_bot import InviteBot, DisconnectBot
from commands.ping import Ping
from commands.pocket_sand import PocketSand
from commands.rps import RockPaperScissors
from commands.shutup_will import ShutupWill
from discord_bot import HuskieBot
from tasks.chat_moderate import ChatModerator
from tasks.gru_nose import GruNosePoster
from tasks.presence_changer import PresenceChanger

if __name__ == '__main__':
    # Config
    logging.basicConfig(level=logging.INFO)
    dotenv.load_dotenv()
    DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')

    client = HuskieBot(commands=[
        EightBall,
        DiceRoll,
        ShutupWill,
        RockPaperScissors,
        DankMemePoster,
        InviteBot,
        DisconnectBot,
        Ping,
        DMCommand,
        PocketSand,
    ], tasks=[
        GruNosePoster,
        ChatModerator,
        PresenceChanger,
    ])
    client.run(DISCORD_BOT_TOKEN)
