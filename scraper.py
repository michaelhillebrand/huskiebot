import re
import time
from datetime import datetime

import pytz
from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from tzlocal import get_localzone


class Scraper(object):

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
            status = driver.find_element_by_id("status").text
            if status != self.previous_status:
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

    def run(self):
        """
        Starts scraping/betting

        :return: None
        """
        try:
            print('Running Scraper...')
            match = None
            start_time = None
            red = None
            blue = None
            # noinspection RegExpSingleCharAlternation
            bet_regex = re.compile(r"\$|,")
            # print('Loading Agent')
            # agent = Agent(None, False)
            # print('Loaded Agent')
            wait = WebDriverWait(self.salty_driver, 100000)
            self.salty_driver.get("http://www.saltybet.com/")
            while True:
                wait.until(self._is_changed)
                alert = self.salty_driver.find_element_by_id("footer-alert").text.strip()

                status = self.previous_status.strip()
                if status:
                    print(status)
                    self.discord_bot.send_to_salt(status)
                    self.salty_driver.implicitly_wait(1)
                    time.sleep(1)
                    if 'open' in status.lower():
                        red_name = self.salty_driver.find_element_by_id("sbettors1")\
                            .find_element_by_class_name('redtext').text.strip()
                        blue_name = self.salty_driver.find_element_by_id("sbettors2")\
                            .find_element_by_class_name('bluetext').text.strip()
                        if 'team' in red_name.lower() or 'team' in blue_name.lower():
                            # teams have too many variables
                            print('Skipping Team match\n--\n')
                            continue
                        alert = self.salty_driver.find_element_by_id("footer-alert").text
                        if 'exhibition' in alert:
                            mode = 'e'
                        elif 'Tournament' in alert:
                            mode = 't'
                        # FINAL ROUND! Stay tuned for exhibitions after the tournament!
                        elif 'bracket' in alert:
                            mode = 't'
                        else:
                            mode = 'm'
                        match = {'red': red, 'blue': blue, 'mode': mode,
                                  'date': datetime.utcnow().replace(tzinfo=pytz.utc).astimezone(get_localzone())}
                        print('-- New Match --')
                        print('{}\tv.\t{}\t({})'.format(red.name, blue.name, mode.title()))
                        print('Total\t{}\t|\t{}'.format(red.matches, blue.matches))
                        print('Wins\t{}\t|\t{}'.format(red.wins, blue.wins))
                        print('Losses\t{}\t|\t{}'.format(red.losses, blue.losses))
                        guess, confidence = agent.guess(match)
                        print('\nPick: {} ({}%)'.format(guess.name, confidence * 100))
                        print('--')
                    elif 'locked' in status.lower():
                        print('Match started')
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
                        match.save()
                        print('Red:\t${} ({})'.format(match.red_bet, match.red_betters))
                        print('Blue:\t${} ({})'.format(match.blue_bet, match.blue_betters))
                        print('Odds:\t{}'.format(match.get_odds()))
                        print('--')
                    elif 'wins' in status.lower():
                        if match is None or start_time is None:
                            continue
                        match.winner = red if red.name == status.split(' wins!')[0].strip() else blue
                        match.time = (datetime.utcnow().replace(tzinfo=pytz.utc)
                                      .astimezone(get_localzone()) - start_time).seconds
                        match.save()
                        print('Match over ({} wins!)'.format(match.winner.name))
                        print('--')
                        match = None
                        start_time = None
        except KeyboardInterrupt:
            # catches CTRL + C
            print('Scraper stopped')
            # try:
            #     # deletes incomplete match
            #     # noinspection PyUnboundLocalVariable
            #     match.delete()
            # except NameError:
            #     pass
