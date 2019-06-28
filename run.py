# Standard library
import logging
import os

# Pip installed libraries
import dotenv

# Local libraries
from commands.dank_meme_poster import DankMemePoster
from commands.dice_roll import DiceRoll
from commands.eight_ball import EightBall
from commands.invite_bot import InviteBot
from commands.rps import RockPaperScissors
from commands.shutup_will import ShutupWill
from discord_bot import HuskieBot
from tasks.gru_nose import GruNosePoster

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
    ], tasks=[
        GruNosePoster,
    ])
    client.run(DISCORD_BOT_TOKEN)
