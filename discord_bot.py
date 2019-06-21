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
        self.gru_channel = None
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

    async def post_gru_nose_pics(self):
        while True:
            now = datetime.datetime.now()
            if now.time().hour == datetime.time(20).hour:
                print("It's 8:00pm!")
                await self.gru_channel.send_file('/home/michael/Pictures/gru_pics/{}.png'.format(now.date()))
            await asyncio.sleep(1200)  # check every hour

    async def url_download(self, message, content):
        await self.wait_until_ready()
        r = requests.get(content[-1], stream=True)
        if r.status_code == 200:
            try:
                with NamedTemporaryFile() as temp:
                    print('Downloading File...')
                    await message.channel.send('{} I am downloading the file. This may take a long time. '
                                               'I will ping you when I finish.'
                                               .format(message.author.mention))
                    for chunk in r.iter_content(chunk_size=4096):
                        if chunk:  # filter out keep-alive new chunks
                            temp.write(chunk)
                        await asyncio.sleep(0.01)
                    temp.flush()
                    temp.seek(0)
                    print('File downloaded!')
                    await message.author.send('Hey, I have finished downloading your file! I am now processing it.')
                    with ZipFile(temp.name, 'r') as zip_file:
                        file_count = len(zip_file.infolist())
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
                await message.author.send('I finished processing your upload of {} images. '
                                          'Shitpost away!'.format(file_count))
            except Exception as e:
                self.log(level=ERROR,
                         user=message.author,
                         message='file failed to upload: {}'.format(e))
                await message.author.send('I got an error while uploading your file: {}'.format(e))

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
                await message.channel.send('{user}\t\t\tHuskieBot\n'
                                           '{user_move}\tvs.\t{bot_move}\n'
                                           'GAME OVER\n'
                                           'Final Score: {user_score}-{bot_score}-{ties}\n\n'
                                           'Want to play again?'
                                           .format(user=message.author.mention,
                                                   user_move=move,
                                                   bot_move=bot_move,
                                                   user_score=game['user_score'],
                                                   bot_score=game['bot_score'],
                                                   ties=game['ties']
                                                   )
                                           )
                self.rps_stats.pop(message.author.id, None)
            else:
                await message.channel.send('{user}\t\t\tHuskieBot\n'
                                           '{user_move}\tvs.\t{bot_move}\n'
                                           'Current Score: {user_score}-{bot_score}-{ties}'
                                           .format(user=message.author.mention,
                                                   user_move=move,
                                                   bot_move=bot_move,
                                                   user_score=game['user_score'],
                                                   bot_score=game['bot_score'],
                                                   ties=game['ties']
                                                   )
                                           )

    async def on_ready(self):
        await self.change_presence(activity=discord.Game(name='Shitposting Memes'))
        self.gru_channel = self.get_channel(537442178289500160)
        self.will = self.get_guild(100708750096080896).get_member_named('ARDelta#9051')
        self.loop.create_task(self.post_gru_nose_pics())
        print('Huskie Bot Online')

    async def on_message(self, message):

        # we do not want the bot to reply to itself
        if message.author == self.user:
            return

        elif message.content.startswith('!commands'):
            await message.channel.send(
                "!roll {int}    - Roll a die with X sides\n"
                "!rps           - Start a Rock, Paper, Scissors game (Best of 3)\n"
                "!dank          - HuskieBot will shitpost a random image it has\n"
                "!upload        - Uploads a single image to HuskieBot for use with \"!dank\" command\n"
                "!bulkupload    - Uploads a ZIP of images to HuskieBot for use with \"!dank\" command\n"
                "!urlupload     - Uploads a ZIP of images to HuskieBot (via URL) for use with \"!dank\" command\n"
                "!shutup        - HuskieBot will tell Will to shutup\n"
            )

        elif message.content.startswith('!roll'):
            content = message.content.split(' ')
            if len(content) != 2:
                await message.channel.send('That is not a valid roll')
            else:
                try:
                    await message.channel.send('{}'.format(randint(1, int(content[-1]))))
                except ValueError:
                    await message.channel.send('That is not a valid roll')

        elif message.content.startswith('!rock'):
            await self.rps_play(message, ROCK)

        elif message.content.startswith('!paper'):
            await self.rps_play(message, PAPER)

        elif message.content.startswith('!scissors'):
            await self.rps_play(message, SCISSORS)

        elif message.content.startswith('!rps'):
            if self.rps_stats.get(message.author.id, None):
                game = self.rps_stats[message.author.id]
                await message.channel.send(
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
                await message.channel.send('Lets play! Send me a move. (!rock, !paper, !scissors)')

        elif message.content.startswith('!dank'):
            images = os.listdir('media/')
            if len(images) == 0:
                await message.channel.send('I don\'t have any images to shitpost with')
            else:
                image = images[randint(0, len(images)) - 1]
                await message.channel.send_file('media/{}'.format(image), filename=image)

        elif message.content.startswith('!upload'):
            if not message.attachments:
                await message.channel.send('No file detected')
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
                            await message.channel.send('Dank image uploaded successfully')
                        except Exception as e:
                            self.log(level=ERROR,
                                     user=message.author,
                                     message='{} failed to upload'.format(attachment['filename']))
                            await message.channel.send('Error: {}'.format(e))

        elif message.content.startswith('!bulkupload'):
            if not message.attachments:
                await message.channel.send('No file detected')
            else:
                await message.channel.send('Processing file...')
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
                            await message.channel.send('Dank ZIP uploaded successfully')
                        except Exception as e:
                            self.log(level=ERROR,
                                     user=message.author,
                                     message='{} failed to upload'.format(attachment['filename']))
                            await message.channel.send('Error: {}'.format(e))

        elif message.content.startswith('!urlupload'):
            content = message.content.split(' ')
            if len(content) != 2:
                await message.channel.send('That is not a valid url')
            else:
                self.loop.create_task(self.url_download(message, content))

        elif message.content.startswith('!shutup'):
            await message.channel.send('{} Shut up!'.format(self.will.mention))

    async def close(self):
        print('Shutting Down...')
        return super().close()
