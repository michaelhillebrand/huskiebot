import asyncio
import os
from io import BytesIO
from random import randint
from tempfile import NamedTemporaryFile
from zipfile import ZipFile

import discord
import requests
from discord.ext import commands
from PIL import Image
from requests import HTTPError

from discord_bot import MEDIA_PATH

class DankMemes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def _process_image(self, file):
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

    # TODO: Fix this. Even with the original bot, my uploads from dropbox or onedrive worked
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
        await self.bot.wait_until_ready()
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

    @commands.command()
    async def dankbulkupload(self, ctx):
        """
        uploads a zip of images from attachments or url to HuskieBot's library

        Parameters
        ----------
        message : discord.Message

        Returns
        -------
        str

        """
        args = ctx.message.content.split(' ')[1:]
        if ctx.message.attachments or len(args) == 1:
            await ctx.send('{} I am downloading the file. This may take a long time. '
                                       'I will ping you when I finish.'
                                       .format(ctx.author.mention))
            file_count = 0
            try:
                zip_file = None
                if ctx.message.attachments:
                    for attachment in ctx.message.attachments:
                        zip_file = await self._download(attachment.url)
                        file_count += len(zip_file.infolist())
                        for file in zip_file.infolist():
                            self._process_image(BytesIO(zip_file.read(file.filename)))
                else:
                    zip_file = await self._download(args[0])
                    file_count += len(zip_file.infolist())
                    for file in zip_file.infolist():
                        self._process_image(BytesIO(zip_file.read(file.filename)))
                zip_file.close()
                await ctx.author.send('I finished processing your upload of {} images. '
                                          'Shitpost away!'.format(file_count))
            except Exception as e:
                await ctx.author.send('I got an error while uploading your file: {}'.format(e))
        elif len(args) > 1:
            await ctx.send('That is not a valid url')
        else:
            await ctx.send('No file or url has been provided')

    @commands.command()
    async def dankupload(self, ctx):
        """
        uploads an image to HuskieBot's library

        Parameters
        ----------
        message : discord.Message

        Returns
        -------
        str

        """
        if not ctx.message.attachments:
            await ctx.send('No file detected')
        else:
            async with ctx.typing():
                for attachment in ctx.message.attachments:
                    response = requests.get(attachment.url)
                    if response.status_code == 200:
                        try:
                            self._process_image(BytesIO(response.content))
                            await ctx.send('Dank image uploaded successfully')
                        except Exception as e:
                            await ctx.send('Error: {}'.format(e))

    @commands.command()
    async def dank(self, ctx):
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
            await ctx.send('I don\'t have any images to shitpost with')
        else:
            try:
                args = ctx.message.content.split(' ')[1:]
                if len(args) > 1:
                    raise RuntimeError
                elif len(args) == 1:
                    index = int(args[0])
                else:
                    index = randint(0, len(images) - 1)
                await ctx.send(index, file=discord.File(os.path.join(MEDIA_PATH, images[index])))
            except (ValueError, RuntimeError, IndexError):
                await ctx.send('That is not a valid meme')
