import logging

from discord.ext import commands

from personalities.base import Personality
from personalities.bojack_horseman import BoJack
from personalities.hank_hill import Hank
from utils.settings import Settings


class HuskieBot(commands.Bot):

    available_personalities = {
        'default': Personality,
        'hank': Hank,
        'bojack': BoJack
    }

    def __init__(self, **options):
        super().__init__(**options)
        self.settings = Settings()

    async def on_ready(self) -> None:
        logging.info('Huskie Bot Online')
