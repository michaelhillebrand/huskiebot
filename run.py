# Standard library
import os

# Pip installed libraries
import dotenv

# Local libraries
from discord_bot import HuskieBot

if __name__ == '__main__':
    # Config
    dotenv.load_dotenv()
    DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')

    try:
        client = HuskieBot()
        client.run(DISCORD_BOT_TOKEN)
    except IndexError:
        print('Key not provided - Unable to start bot')
