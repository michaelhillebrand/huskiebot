import asyncio
from threading import Lock, Thread

import discord
from discord import Channel, Server

from scraper import Scraper

mutex = Lock()


class HuskieBot(discord.Client):

    def __init__(self, *, loop=None, **options):
        self.scraper = Scraper(self)
        self.salt_channel = Channel(**{'id': '555186709772501013', 'server': Server(**{'id': '100708750096080896'})})
        super().__init__(loop=loop, **options)

    def send_to_salt(self, message):
        self.loop.create_task(self.send_message(self.salt_channel, message))

    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')

    async def on_message(self, message):

        # we do not want the bot to reply to itself
        if message.author == self.user:
            return

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
