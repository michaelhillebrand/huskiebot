import asyncio
import os
from io import BytesIO
from random import randint
from tempfile import NamedTemporaryFile
from zipfile import ZipFile

import discord
import requests
from PIL import Image
from requests import HTTPError

from commands.base import BaseCommand
from discord_bot import MEDIA_PATH


def _process_image(file):
    """
    processes image/gif and saves it to hard drive

    Parameters
    ----------
    file : BytesIO

    Returns
    -------
    None

    """
    file.seek(0)
    image = Image.open(file)
    if image.format == 'GIF':
        image.save(os.path.join(MEDIA_PATH, '{}.gif'.format(len(os.listdir(MEDIA_PATH)))),
                   save_all=True,
                   optimize=True
                   )
    else:
        image = image.convert(mode='RGB')
        image.save(os.path.join(MEDIA_PATH, '{}.jpg'.format(len(os.listdir(MEDIA_PATH)))),
                   format='JPEG',
                   optimize=True
                   )


class DankMemeBulkUpload(BaseCommand):
    trigger = 'dankbulkupload'
    description = 'Uploads a ZIP of images to HuskieBot (via attachments or URL) for use with "!dank" command'

    async def _download(self, url):
        """
        downlaods ZIP file from url

        Parameters
        ----------
        url : str

        Returns
        -------
        ZipFile

        """
        await self.client.wait_until_ready()
        r = requests.get(url, stream=True)
        if r.status_code == 200:
            with NamedTemporaryFile() as temp:
                for chunk in r.iter_content(chunk_size=4096):
                    if chunk:  # filter out keep-alive new chunks
                        temp.write(chunk)
                    await asyncio.sleep(0.01)  # allows HuskieBot to respond to other requests
                temp.flush()
                temp.seek(0)
                return ZipFile(temp.name, 'r')
        else:
            raise HTTPError('Received a non 200 status code: {}'.format(r.status_code))

    async def command(self, message):
        """
        uploads a zip of images from attachments or url to HuskieBot's library

        Parameters
        ----------
        message : discord.Message

        Returns
        -------
        str

        """
        args = message.content.split(' ')[1:]
        if message.attachments or len(args) == 1:
            await message.channel.send('{} I am downloading the file. This may take a long time. '
                                       'I will ping you when I finish.'
                                       .format(message.author.mention))
            file_count = 0
            try:
                zip_file = None
                if message.attachments:
                    for attachment in message.attachments:
                        zip_file = await self._download(attachment.url)
                        file_count += len(zip_file.infolist())
                        for file in zip_file.infolist():
                            _process_image(BytesIO(zip_file.read(file.filename)))
                else:
                    zip_file = await self._download(args[0])
                    file_count += len(zip_file.infolist())
                    for file in zip_file.infolist():
                        _process_image(BytesIO(zip_file.read(file.filename)))
                zip_file.close()
                await message.author.send('I finished processing your upload of {} images. '
                                          'Shitpost away!'.format(file_count))
            except Exception as e:
                await message.author.send('I got an error while uploading your file: {}'.format(e))
        elif len(args) > 1:
            await message.channel.send('That is not a valid url')
        else:
            await message.channel.send('No file or url has been provided')


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
                            _process_image(BytesIO(response.content))
                            await message.channel.send('Dank image uploaded successfully')
                        except Exception as e:
                            await message.channel.send('Error: {}'.format(e))


class DankMemePoster(BaseCommand):
    trigger = 'dank'
    description = 'HuskieBot will shitpost a random image it has'

    async def on_ready(self):
        await self.client.add_commands([
            DankMemeUpload,
            DankMemeBulkUpload
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
        images = sorted(os.listdir(MEDIA_PATH))
        if len(images) == 0:
            await message.channel.send('I don\'t have any images to shitpost with')
        else:
            try:
                args = message.content.split(' ')[1:]
                if len(args) > 1:
                    raise RuntimeError
                elif len(args) == 1:
                    index = int(args[0])
                else:
                    index = randint(0, len(images) - 1)
                await message.channel.send(index, file=discord.File(os.path.join(MEDIA_PATH, images[index])))
            except (ValueError, RuntimeError, IndexError):
                await message.channel.send('That is not a valid meme')
