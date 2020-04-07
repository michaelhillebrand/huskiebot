import logging
import os

from discord.ext import tasks
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from cogs import BASE_PATH
from cogs.base import BaseCog


class SaltyBet(BaseCog):
    ALERT_THRESHOLD = 10  # matches

    def __init__(self, bot) -> None:
        self.channel_id = int(os.getenv('SALTY_CHANNEL'))
        self.channel = None
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        self.salty_driver = webdriver.Chrome(os.path.join(BASE_PATH, 'drivers/chromedriver'),
                                             chrome_options=chrome_options)
        self.salty_driver.get("https://www.saltybet.com/authenticate?signin=1")
        self.salty_driver.find_element_by_id("email").send_keys(os.getenv('SALTY_USERNAME'))
        self.salty_driver.find_element_by_id("pword").send_keys(os.getenv('SALTY_PASSWORD'))
        self.salty_driver.find_element_by_id("signinform").submit()
        if self.channel_id:
            self.tourney_alert.start()
        else:
            logging.warning('No channel ID was provided')
        super().__init__(bot)

    def cog_unload(self):
        self.tourney_alert.cancel()

    @tasks.loop(minutes=30)
    async def tourney_alert(self):
        """
        HuskieBot will check saltybet.com to see if a tourney is about to start
        """
        logging.info("Checking for Salty Bet tourney")
        self.salty_driver.get("https://www.saltybet.com/shaker")
        status = self.salty_driver.find_element_by_xpath("//div[@id='compendiumleft']/div[1]").text.split(' ', 1)
        if 'more matches until the next tournament' in status[-1]:
            matches_left = int(status[0])
            if matches_left < self.ALERT_THRESHOLD or os.getenv('ENVIRONMENT') == 'development':
                await self.channel.send(f'@Salt {matches_left} matches left until tournament')

    @tourney_alert.before_loop
    async def before_tourney_alert(self):
        await self.bot.wait_until_ready()
        channel = self.bot.get_channel(self.channel_id)
        if channel:
            self.channel = channel
        else:
            logging.error('Channel ID was invalid')
            raise ValueError
