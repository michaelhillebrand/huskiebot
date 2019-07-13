import logging
import os

from discord.ext import commands

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
MEDIA_PATH = os.path.join(BASE_PATH, 'media/')
if not os.path.exists(MEDIA_PATH):
    os.makedirs(MEDIA_PATH)


class HuskieBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def on_ready(self):
        logging.info('Huskie Bot Online')
