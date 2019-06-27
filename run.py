# Standard library
import logging
import os

# Pip installed libraries
import dotenv

# Local libraries
from discord_bot import HuskieBot

if __name__ == '__main__':
    # Config
    logging.basicConfig(level=logging.INFO)
    dotenv.load_dotenv()
    DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')

    # Setup

    if not os.path.exists('media'):
        os.makedirs('media')

    try:
        client = HuskieBot()
        client.run(DISCORD_BOT_TOKEN)
    except IndexError:
        print('Key not provided - Unable to start bot')
