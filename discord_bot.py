import asyncio
from threading import Lock, Thread

import discord
from discord import Channel, Server

from scraper import Scraper

mutex = Lock()


class HuskieBot(discord.Client):

    def __init__(self, *, loop=None, **options):
        self.scraper = Scraper(self)
        self.doc_bop = None
        self.salt_channel = None
        self.will = None
        super().__init__(loop=loop, **options)

    def send_to_salt(self, message):
        self.loop.create_task(self.send_message(self.salt_channel, message))

    async def on_ready(self):
        await self.change_presence(game=discord.Game(name='Salty Bet'))
        self.doc_bop = self.get_server('100708750096080896')
        self.salt_channel = self.doc_bop.get_channel('555186709772501013')
        self.will = self.doc_bop.get_member_named('ARDelta#9051')
        message = '////////////////////\n' \
                  '////////////////////\n' \
                  '////**HuskieBot**////\n' \
                  '///**Initialized**///\n' \
                  '///////////////////\n' \
                  '///////////////////\n\n' \
                  'For a list of available commands, type !commands'
        self.send_to_salt(message)

    async def on_message(self, message):

        # we do not want the bot to reply to itself
        if message.author == self.user:
            return

        elif message.content.startswith('!commands'):
            await self.send_message(message.channel,
                                    "hello\t\t- Say hi to Huskie Bot\n"
                                    "status\t\t- Display status of HuskieBot\n"
                                    "learn\t\t- Starts HuskieBot\'s learning algorithm "
                                    "(This will disable most commands while it is running\n"
                                    "stoplearn\t\t- Stops Huskie Bot\'s learning\n"
                                    "mute\t\t- Stops HuskieBot from posting stats about Salty Bet matches\n"
                                    "unmute\t\t- Huskie Bot will post stats about Salty Bet matches\n"
                                    "shutup\t\t- Huskie Bot will tell Will to shutup\n"
                                    )

        elif message.content.startswith('!status'):
            await self.send_message(message.channel, 'Learning: {}'.format(mutex.locked()))

        elif message.content.startswith('!stoplearn'):
            mutex.release()
            await self.send_message(message.channel, 'Stopped learning')

        elif mutex.locked():
            await self.send_message(message.channel, 'I am learning right now and unable to perform any actions\n'
                                                     'Type "!stoplearn" to stop learning')

        elif message.content.startswith('!hello'):
            msg = 'Hello {0.author.mention}'.format(message)
            await self.send_message(message.channel, msg)

        elif message.content.startswith('!learn'):
            mutex.acquire()
            await self.send_message(message.channel, 'Started learning...\n'
                                                     'Commands will unavailable!\n'
                                                     'Type "!stoplearn" to stop learning')

        elif message.content.startswith('!mute'):
            self.scraper.mute()
            await self.send_message(message.channel, 'I am muted')

        elif message.content.startswith('!unmute'):
            self.scraper.unmute()
            await self.send_message(message.channel, 'I am free to speak!')

        elif message.content.startswith('!scrape'):
            Thread(target=self.scraper.run).start()
            await self.send_message(message.channel, 'Started scraping...')

        elif message.content.startswith('!stopscrape'):
            self.scraper.stop()
            await self.send_message(message.channel, 'Stopped scraping')

        elif message.content.startswith('!shutup'):
            self.scraper.stop()
            await self.send_message(message.channel, '{} Shut up!'.format(self.will.mention))

    async def close(self):
        await self.send_message(self.salt_channel, 'Shutting Down...')
        return super().close()
