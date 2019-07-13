import datetime
import logging
import os

import discord
from discord.ext import tasks, commands

from discord_bot import BASE_PATH


class GruNosePoster(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.channel_id = os.getenv('DISCORD_BOT_TOKEN')
        if self.channel_id:
            self.gru_nose_poster.start()
        else:
            logging.warning('No channel id was provided')

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
        channel = self.bot.get_channel(self.channel_id)
        now = datetime.datetime.now()
        if now.hour == 12:  # Noon
            logging.info("It's high noon! Attempting to post the latest gru nose picture")
            gru_nose_filepath = os.path.join(BASE_PATH, 'gru/{}.png'.format(now.date()))
            try:
                logging.info("Posting file: {file}".format(file = gru_nose_filepath))
                await channel.send(file=discord.File(gru_nose_filepath))
            except FileNotFoundError as e:
                logging.error("Failed to find file: {}".format(e.filename))
                self.gru_nose_poster.cancel()
                return
        # set next posting time
        # hours_until = 11 - now.hour
        # hours_until = 24 + hours_until if hours_until < 0 else hours_until
        # self.gru_nose_poster.cancel()
        # self.gru_nose_poster.change_interval(hours=hours_until, minutes=60 - now.minute)
        # self.gru_nose_poster.start()

    # TODO: Switch this to happen in a bot.event on_ready function instead
    @gru_nose_poster.before_loop
    async def before_gru_nose_poster(self):
        logging.info('Waiting for bot to be ready...')
        await self.bot.wait_until_ready()
