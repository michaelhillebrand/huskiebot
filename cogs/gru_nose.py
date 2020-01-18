import datetime
import logging
import os

import discord
from discord.ext import tasks

from cogs import BASE_PATH
from cogs.base import BaseCog


class GruNosePoster(BaseCog):

    def __init__(self, bot) -> None:
        self.channel_id = int(os.getenv('GRU_NOSE_CHANNEL'))
        self.channel = None
        if self.channel_id:
            self.gru_nose_poster.start()
        else:
            logging.warning('No channel ID was provided')
        super().__init__(bot)

    def cog_unload(self):
        self.gru_nose_poster.cancel()

    @tasks.loop(hours=1)
    async def gru_nose_poster(self):
        """
        HuskieBot will post the latest gru nose picture everyday at 12:00pm

        Returns
        -------
        discord.File
            The latest gru nose picture
        """
        logging.info("Checking to see if it is time to post a Gru nose picture")
        now = datetime.datetime.now()
        if now.hour == 22:  # Noon
            logging.info("It's high noon! Attempting to post the latest gru nose picture")
            gru_nose_filepath = os.path.join(BASE_PATH, f'gru/{now.date()}.png')
            try:
                logging.info(f"Posting file: {gru_nose_filepath}")
                await self.channel.send(file=discord.File(gru_nose_filepath))
            except FileNotFoundError as e:
                logging.error(f"Failed to find file: {e.filename}")
                self.gru_nose_poster.cancel()
                return
        # # set next posting time
        # hours_until = 11 - now.hour
        # hours_until = 24 + hours_until if hours_until < 0 else hours_until
        # self.gru_nose_poster.change_interval(hours=hours_until, minutes=60 - now.minute)

    @gru_nose_poster.before_loop
    async def before_gru_nose_poster(self):
        await self.bot.wait_until_ready()
        channel = self.bot.get_channel(self.channel_id)
        if channel:
            self.channel = channel
        else:
            logging.error('Channel ID was invalid')
            raise ValueError
