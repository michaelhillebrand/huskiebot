import logging

from discord.ext import commands

from personalities.base import Personality
from personalities.bojack_horseman import BoJack
from personalities.hank_hill import Hank
from personalities.redditor import Redditor
from utils.settings import Settings


class HuskieBot(commands.Bot):

    available_personalities = {
        Personality.slug: Personality,
        Hank.slug: Hank,
        BoJack.slug: BoJack,
        Redditor.slug: Redditor,
    }

    def __init__(self, **options):
        super().__init__(**options)
        self.settings = Settings()

    async def on_ready(self) -> None:
        logging.info('Huskie Bot Online')
