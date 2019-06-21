import asyncio
import datetime
import os
from io import BytesIO
from random import randint
from tempfile import NamedTemporaryFile
from zipfile import ZipFile

import discord
import math
import requests
from PIL import Image

INFO = 'Info'
SUCCESS = 'Success'
WARNING = 'Warning'
ERROR = 'Error'

BEST_OF = 3

ROCK = 'Rock'
PAPER = 'Paper'
SCISSORS = 'Scissors'

RPS_CHOICES = [ROCK, PAPER, SCISSORS]


class HuskieBot(discord.Client):

    def __init__(self, *, loop=None, **options):
        self.doc_bop = None
        self.salt_channel = None
        self.will = None
        self.media_dir = 'media/'
        self.rps_stats = {}
        super().__init__(loop=loop, **options)

    def log(self, level=INFO, user=None, message=None):
        log = open('upload.log', 'a')
        log.write('[{time}] [{level}] [{user}] {message}\n'
                  .format(time=datetime.datetime.now(),
                          level=level,
                          user=user,
                          message=message))
        log.close()

    async def url_download(self, message, content):
        await self.wait_until_ready()
        r = requests.get(content[-1], stream=True)
        if r.status_code == 200:
            try:
                with NamedTemporaryFile() as temp:
                    print('Downloading File...')
                    await self.send_message(message.channel, 'Downloading file...')
                    for chunk in r.iter_content(chunk_size=1024):
                        if chunk:  # filter out keep-alive new chunks
                            temp.write(chunk)
                        await asyncio.sleep(0.01)
                    temp.flush()
                    temp.seek(0)
                    print('File downloaded!')
                    await self.send_message(message.channel, 'File downloaded!')
                    with ZipFile(temp.name, 'r') as zip_file:
                        for file in zip_file.infolist():
                            image = Image.open(BytesIO(zip_file.read(file.filename)))
                            image = image.convert(mode='RGB')
                            image.save(self.media_dir + '{}.jpg'.format(len(os.listdir('media/')) + 1),
                                       format='JPEG',
                                       optimize=True
                                       )
                self.log(level=SUCCESS,
                         user=message.author,
                         message='file uploaded')
                await self.send_message(message.channel, 'Dank ZIP uploaded successfully')
            except Exception as e:
                self.log(level=ERROR,
                         user=message.author,
                         message='file failed to upload')
                await self.send_message(message.channel, 'Error: {}'.format(e))

    async def rps_play(self, message, move):
        if self.rps_stats.get(message.author.id, None):
            bot_move = RPS_CHOICES[randint(0, len(RPS_CHOICES) - 1)]
            if bot_move == move:
                result = 0
            elif (bot_move == ROCK and move == PAPER) or \
                    (bot_move == PAPER and move == SCISSORS) or \
                    (bot_move == SCISSORS and move == ROCK):
                result = 1
            elif (bot_move == ROCK and move == SCISSORS) or \
                    (bot_move == PAPER and move == ROCK) or \
                    (bot_move == SCISSORS and move == PAPER):
                result = -1
            else:
                result = -2
            game = self.rps_stats[message.author.id]
            game['turn'] += 1
            game['history'].append({'bot': bot_move, 'user': move, 'result': result})
            if result == 1:
                game['user_score'] += 1
            elif result == -1:
                game['bot_score'] += 1
            elif result == 0:
                game['ties'] += 1
            if max(game['user_score'], game['bot_score']) >= math.ceil(BEST_OF/2):
                await self.send_message(message.channel, 'User\t\t\tHuskieBot\n'
                                                         '{user_move}\tvs.\t{bot_move}\n'
                                                         'GAME OVER\n'
                                                         'Final Score: {user_score}-{bot_score}-{ties}\n\n'
                                                         'Want to play again?'
                                        .format(user_move=move,
                                                bot_move=bot_move,
                                                user_score=game['user_score'],
                                                bot_score=game['bot_score'],
                                                ties=game['ties']
                                                )
                                        )
                self.rps_stats.pop(message.author.id, None)
            else:
                await self.send_message(message.channel, 'User\t\t\tHuskieBot\n'
                                                         '{user_move}\tvs.\t{bot_move}\n'
                                                         'Current Score: {user_score}-{bot_score}-{ties}'
                                        .format(user_move=move,
                                                bot_move=bot_move,
                                                user_score=game['user_score'],
                                                bot_score=game['bot_score'],
                                                ties=game['ties']
                                                )
                                        )

    async def on_ready(self):
        await self.change_presence(game=discord.Game(name='Shitposting Memes'))
        self.doc_bop = self.get_server('100708750096080896')
        self.salt_channel = self.doc_bop.get_channel('555186709772501013')
        self.will = self.doc_bop.get_member_named('ARDelta#9051')
        print('Huskie Bot Online')

    async def on_message(self, message):

        # we do not want the bot to reply to itself
        if message.author == self.user:
            return

        elif message.content.startswith('!commands'):
            await self.send_message(message.channel,
                                    "!roll {int}    - Roll a die with X sides\n"
                                    "!rps           - Start a Rock, Paper, Scissors game (Best of 3)\n"
                                    "!dank          - HuskieBot will shitpost a random image it has\n"
                                    "!upload        - Uploads a single image to HuskieBot for use with \"!dank\" command\n"
                                    "!bulkupload    - Uploads a ZIP of images to HuskieBot for use with \"!dank\" command\n"
                                    "!shutup        - HuskieBot will tell Will to shutup\n"
                                    )

        elif message.content.startswith('!roll'):
            content = message.content.split(' ')
            if len(content) != 2:
                await self.send_message(message.channel, 'That is not a valid roll')
            else:
                try:
                    await self.send_message(message.channel, '{}'.format(randint(1, int(content[-1]))))
                except ValueError:
                    await self.send_message(message.channel, 'That is not a valid roll')

        elif message.content.startswith('!rock'):
            await self.rps_play(message, ROCK)

        elif message.content.startswith('!paper'):
            await self.rps_play(message, PAPER)

        elif message.content.startswith('!rock'):
            await self.rps_play(message, SCISSORS)

        elif message.content.startswith('!rps'):
            if self.rps_stats.get(message.author.id, None):
                game = self.rps_stats[message.author.id]
                await self.send_message(message.channel,
                                        'I already have a game started with you.\n'
                                        'We are on turn {} with a best of {}.\n'
                                        'The current score is {}-{}-{}'
                                        .format(game['turn'],
                                                BEST_OF,
                                                game['user_score'],
                                                game['bot_score'],
                                                game['ties']))
            else:
                self.rps_stats.update({message.author.id: {
                    'turn': 1,
                    'history': [],
                    'user_score': 0,
                    'bot_score': 0,
                    'ties': 0,
                }})
                await self.send_message(message.channel, 'Lets play! Send me a move. (!rock, !paper, !scissors)')

        elif message.content.startswith('!dank'):
            images = os.listdir('media/')
            if len(images) == 0:
                await self.send_message(message.channel, 'I don\'t have any images to shitpost with')
            else:
                image = images[randint(0, len(images)) - 1]
                await self.send_file(message.channel, 'media/{}'.format(image), filename=image)

        elif message.content.startswith('!upload'):
            if not message.attachments:
                await self.send_message(message.channel, 'No file detected')
            else:
                for attachment in message.attachments:
                    response = requests.get(attachment['url'])
                    if response.status_code == 200:
                        try:
                            image = Image.open(BytesIO(response.content))
                            image = image.convert(mode='RGB')
                            image.save(self.media_dir + '{}.jpg'.format(len(os.listdir('media/')) + 1),
                                       format='JPEG',
                                       optimize=True
                                       )
                            self.log(level=SUCCESS,
                                     user=message.author,
                                     message='{} uploaded'.format(attachment['filename']))
                            await self.send_message(message.channel, 'Dank image uploaded successfully')
                        except Exception as e:
                            self.log(level=ERROR,
                                     user=message.author,
                                     message='{} failed to upload'.format(attachment['filename']))
                            await self.send_message(message.channel, 'Error: {}'.format(e))

        elif message.content.startswith('!bulkupload'):
            if not message.attachments:
                await self.send_message(message.channel, 'No file detected')
            else:
                await self.send_message(message.channel, 'Processing file...')
                for attachment in message.attachments:
                    response = requests.get(attachment['url'])
                    if response.status_code == 200:
                        try:
                            with NamedTemporaryFile() as temp:
                                temp.write(response.content)
                                temp.seek(0)
                                with ZipFile(temp.name, 'r') as zip_file:
                                    for file in zip_file.infolist():
                                        image = Image.open(BytesIO(zip_file.read(file.filename)))
                                        image = image.convert(mode='RGB')
                                        image.save(self.media_dir + '{}.jpg'.format(len(os.listdir('media/')) + 1),
                                                   format='JPEG',
                                                   optimize=True
                                                   )
                            self.log(level=SUCCESS,
                                     user=message.author,
                                     message='{} uploaded'.format(attachment['filename']))
                            await self.send_message(message.channel, 'Dank ZIP uploaded successfully')
                        except Exception as e:
                            self.log(level=ERROR,
                                     user=message.author,
                                     message='{} failed to upload'.format(attachment['filename']))
                            await self.send_message(message.channel, 'Error: {}'.format(e))

        elif message.content.startswith('!urlupload'):
            content = message.content.split(' ')
            if len(content) != 2:
                await self.send_message(message.channel, 'That is not a valid url')
            else:
                self.loop.create_task(self.url_download(message, content))

        elif message.content.startswith('!shutup'):
            await self.send_message(message.channel, '{} Shut up!'.format(self.will.mention))

    async def close(self):
        print('Shutting Down...')
        return super().close()
