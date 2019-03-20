import re
import time
from datetime import datetime

import pytz
from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from tzlocal import get_localzone

from models import Match


class Scraper(object):
    ALERT_TOURNAMENT = 10

    def __init__(self, discord_bot) -> None:
        """
        This initializes the Chrome webdriver in headless mode
        """
        print('Initializing scraper')
        super().__init__()
        self.discord_bot = discord_bot
        self.stop_scrape = False
        self.muted = False
        self.previous_status = ''
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        self.salty_driver = webdriver.Chrome('drivers/chromedriver', chrome_options=chrome_options)
        print('Scraper ready')

    def _is_changed(self, driver):
        """
        Checks to see is the Status has changed as a basis to start scraping

        :param driver:
        :return: boolean
        """
        if self.stop_scrape:
            raise KeyboardInterrupt
        try:
            status = re.sub(r'[^\x00-\x7F]+', '', driver.find_element_by_id("status").text.strip())
            if status and status != self.previous_status:
                self.previous_status = status
                return True
            else:
                return False
        except StaleElementReferenceException:
            # Page was in mid refresh and "status" was not available on the DOM
            return False

    def mute(self):
        self.muted = True

    def unmute(self):
        self.muted = False

    def stop(self):
        self.stop_scrape = True

    def close(self):
        """
        Shuts down the webdriver

        :return: None
        """
        self.salty_driver.close()
        print('Stopping Scraper')

    def emit(self, message):
        if not self.muted:
            print(message)
            self.discord_bot.send_to_salt(message)

    def run(self):
        """
        Starts scraping/betting

        :return: None
        """
        try:
            print('Running Scraper...')
            match = None
            start_time = None
            red_name = None
            blue_name = None
            # noinspection RegExpSingleCharAlternation
            bet_regex = re.compile(r"\$|,")
            # print('Loading Agent')
            # agent = Agent(None, False)
            # print('Loaded Agent')
            wait = WebDriverWait(self.salty_driver, 100000)
            self.salty_driver.get("http://www.saltybet.com/")
            while True:
                wait.until(self._is_changed)
                status = self.previous_status
                self.salty_driver.implicitly_wait(1)
                time.sleep(1)
                alert = self.salty_driver.find_element_by_id("footer-alert").get_attribute('textContent').strip()
                if 'open' in status.lower():
                    self.emit(status)
                    red_name = self.salty_driver.find_element_by_id("sbettors1")\
                        .find_element_by_class_name('redtext').text.strip()
                    blue_name = self.salty_driver.find_element_by_id("sbettors2")\
                        .find_element_by_class_name('bluetext').text.strip()

                    if 'team' in red_name.lower() or 'team' in blue_name.lower():
                        # teams have too many variables
                        self.emit('Skipping Team match')
                        continue

                    if 'exhibition' in alert:
                        mode = Match.EXHIBITION
                    elif 'Tournament' in alert:
                        mode = Match.TOURNAMENT
                    elif 'bracket' in alert:
                        mode = Match.TOURNAMENT
                    else:
                        mode = Match.MATCHMAKING

                    match = Match(**{'red': red_name, 'blue': blue_name, 'mode': mode,
                                     'date': datetime.utcnow().replace(tzinfo=pytz.utc).astimezone(get_localzone())})

                    # guess, confidence = agent.guess(match)
                    # self.emit('-- New Match --'
                    #           '\n{}\tv.\t{}\t({})'
                    #           '\nTotal\t{}\t|\t{}'
                    #           '\nWins\t{}\t|\t{}'
                    #           '\nLosses\t{}\t|\t{}'
                    #           '\n\nPick: {} ({}%)'.format(red.name, blue.name, mode.title(), red.matches,
                    #                                       blue.matches, red.wins, blue.wins, red.losses,
                    #                                       blue.losses, guess.name, confidence * 100))
                elif 'locked' in status.lower():
                    self.emit(status)
                    if match is None:
                        continue
                    start_time = datetime.utcnow().replace(tzinfo=pytz.utc).astimezone(get_localzone())
                    bet_string = self.salty_driver.find_element_by_id("odds").text
                    bets = [bet_regex.sub('', b) for b in bet_string.split(' ') if '$' in b]
                    match.red_betters = int(self.salty_driver.find_element_by_id("sbettors1")
                                            .find_element_by_class_name('redtext').text.split('|')[0].strip())
                    match.blue_betters = int(self.salty_driver.find_element_by_id("sbettors2")
                                             .find_element_by_class_name('bluetext').text.split('|')[-1].strip())
                    try:
                        match.red_bet = int(bets[0])
                        match.blue_bet = int(bets[-1])
                    except IndexError:
                        pass
                    self.emit('Red:\t${} ({})'
                              '\nBlue:\t${} ({})'
                              '\nOdds:\t{}'.format(match.red_bet, match.red_betters, match.blue_bet,
                                                   match.blue_betters, match.get_odds()))
                elif 'wins' in status.lower():
                    self.emit(status)
                    if match is None or start_time is None:
                        continue
                    match.winner = match.red if match.red == status.split(' wins!')[0].strip() else match.blue
                    match.time = (datetime.utcnow().replace(tzinfo=pytz.utc)
                                  .astimezone(get_localzone()) - start_time).seconds
                    match.create()
                    match = None
                    start_time = None
                    if 'more matches until the next tournament' in alert:
                        data = alert.split(' ')
                        if data[0] == self.ALERT_TOURNAMENT:
                            self.discord_bot.send_to_salt('@Salt {}'.format(alert))
                        else:
                            self.emit(alert)
                    elif alert:
                        self.emit(alert)
        except KeyboardInterrupt:
            # catches CTRL + C
            print('Scraper stopped')
            # try:
            #     # deletes incomplete match
            #     # noinspection PyUnboundLocalVariable
            #     match.delete()
            # except NameError:
            #     pass
