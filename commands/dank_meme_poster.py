import asyncio
import os
from io import BytesIO
from random import randint
from tempfile import NamedTemporaryFile
from zipfile import ZipFile

import discord
import requests
from PIL import Image

from commands.base import BaseCommand


class DankMemeUrlUpload(BaseCommand):
    trigger = 'dankurlupload'
    description = 'Uploads a ZIP of images to HuskieBot (via URL) for use with "!dank" command'

    async def _download(self, message):
        await self.client.wait_until_ready()
        try:
            r = requests.get(message.content[-1], stream=True)
            if r.status_code == 200:
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
                            image.save(os.path.join(self.client.media_dir,
                                                    '{}.jpg'.format(
                                                        len(os.listdir(self.client.media_dir))
                                                    )),
                                       format='JPEG',
                                       optimize=True
                                       )
                await message.author.send('I finished processing your upload of {} images. '
                                          'Shitpost away!'.format(file_count))
        except Exception as e:
            await message.author.send('I got an error while uploading your file: {}'.format(e))

    async def command(self, message):
        """
        uploads a zip of images from a url to HuskieBot's library

        Parameters
        ----------
        message : discord.Message

        Returns
        -------
        str

        """
        args = message.content.split(' ')[1:]
        if len(args) != 1:
            await message.channel.send('That is not a valid url')
        else:
            self.client.loop.create_task(self._download(message))


class DankMemeBulkUpload(BaseCommand):
    trigger = 'dankbulkupload'
    description = 'Uploads a ZIP of images to HuskieBot for use with "!dank" command'

    async def command(self, message):
        """
        uploads a zip of images to HuskieBot's library

        Parameters
        ----------
        message : discord.Message

        Returns
        -------
        str

        """
        if not message.attachments:
            await message.channel.send('No file detected')
        else:
            async with message.channel.typing():
                await message.channel.send('Processing file...')
                for attachment in message.attachments:
                    response = requests.get(attachment.url)
                    if response.status_code == 200:
                        try:
                            with NamedTemporaryFile() as temp:
                                temp.write(response.content)
                                temp.seek(0)
                                with ZipFile(temp.name, 'r') as zip_file:
                                    for file in zip_file.infolist():
                                        image = Image.open(BytesIO(zip_file.read(file.filename)))
                                        image = image.convert(mode='RGB')
                                        image.save(os.path.join(self.client.media_dir,
                                                                '{}.jpg'.format(
                                                                    len(os.listdir(self.client.media_dir))
                                                                )),
                                                   format='JPEG',
                                                   optimize=True
                                                   )
                            await message.channel.send('Dank ZIP uploaded successfully')
                        except Exception as e:
                            await message.channel.send('Error: {}'.format(e))


class DankMemeUpload(BaseCommand):
    trigger = 'dankupload'
    description = 'Uploads a single image to HuskieBot for use with "!dank" command'

    async def command(self, message):
        """
        uploads an image to HuskieBot's library

        Parameters
        ----------
        message : discord.Message

        Returns
        -------
        str

        """
        if not message.attachments:
            await message.channel.send('No file detected')
        else:
            async with message.channel.typing():
                for attachment in message.attachments:
                    response = requests.get(attachment.url)
                    if response.status_code == 200:
                        try:
                            image = Image.open(BytesIO(response.content))
                            image = image.convert(mode='RGB')
                            image.save(os.path.join(self.client.media_dir,
                                                    '{}.jpg'.format(len(os.listdir(self.client.media_dir)))),
                                       format='JPEG',
                                       optimize=True
                                       )
                            await message.channel.send('Dank image uploaded successfully')
                        except Exception as e:
                            await message.channel.send('Error: {}'.format(e))


class DankMemePoster(BaseCommand):
    trigger = 'dank'
    description = 'HuskieBot will shitpost a random image it has'

    async def on_ready(self):
        await self.client.add_commands([
            DankMemeUpload
        ])

    async def command(self, message):
        """
        HuskieBot shitposts an image from its library

        Parameters
        ----------
        message : discord.Message

        Returns
        -------
        discord.File
            Dank Image

        """
        images = os.listdir(self.client.media_dir)
        if len(images) == 0:
            await message.channel.send('I don\'t have any images to shitpost with')
        else:
            try:
                args = message.content.split(' ')[1:]
                if len(args) > 1:
                    raise RuntimeError
                elif len(args) == 1:
                    index = int(args)
                else:
                    index = randint(0, len(images) - 1)
                await message.channel.send(index, file=discord.File(os.path.join(self.client.media_dir, images[index])))
            except (ValueError, RuntimeError, IndexError):
                await message.channel.send('That is not a valid meme')
