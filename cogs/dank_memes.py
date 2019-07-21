import logging
import os
import typing
from io import BytesIO
from random import randint
from zipfile import ZipFile

import discord
from PIL import Image
from discord.ext import commands

from cogs import MEDIA_PATH
from cogs.base import BaseCog
from utils.download import download


class DankMemes(BaseCog):

    async def _process_image(self, file):
        """
        Processes image/gif and saves it to hard drive

        Parameters
        ----------
        file : BytesIO / NamedTemporaryFile

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

    async def _bulk_process(self, url):
        """
        Helper function for the dankbulkupload command

        Parameters
        ----------
        url : file to download

        Returns
        -------
        int
            the number of files extracted
        """
        zip_file = ZipFile(await download(url))
        file_count = len(zip_file.infolist())
        for file in zip_file.infolist():
            await self._process_image(BytesIO(zip_file.read(file.filename)))
        zip_file.close()
        return file_count

    @commands.command()
    async def dankbulkupload(self, ctx, url: typing.Optional[str]):
        """
        Uploads a zip of images from attachments or url to HuskieBot's library

        Parameters
        ----------
        ctx : discord.ext.commands.Context
        url : str (optional)

        Returns
        -------
        str

        """
        file_count = 0
        if ctx.message.attachments or url:
            await ctx.send('{} I am downloading the file. This may take a long time. '
                           'I will ping you when I finish.'.format(ctx.author.mention))
        if ctx.message.attachments or url:
            for attachment in ctx.message.attachments:
                file_count += await self._bulk_process(attachment.url)
        elif url:
            file_count += await self._bulk_process(url)
        else:
            await ctx.send('No file or url has been provided')
            return
        logging.info('Successfully added {} images to MEDIA'.format(file_count))
        await ctx.author.send('I finished processing your upload of {} images. '
                              'Shitpost away!'.format(file_count))

    @dankbulkupload.error
    async def on_dankbulkupload_error(self, ctx, error):
        logging.error(error)
        await ctx.author.send(error)

    @commands.command()
    async def dankupload(self, ctx):
        """
        Uploads an image to HuskieBot's library

        Parameters
        ----------
        ctx : discord.ext.commands.Context

        Returns
        -------
        str

        """
        if not ctx.message.attachments:
            await ctx.send('No file detected')
        else:
            async with ctx.typing():
                for attachment in ctx.message.attachments:
                    file = await download(attachment.url)
                    await self._process_image(file)
                    await ctx.send('Dank image uploaded successfully')

    @dankupload.error
    async def on_dankupload_error(self, ctx, error):
        logging.error(error)
        await ctx.channel.send('I got an error while uploading your file: {}'.format(error))

    @commands.group(invoke_without_command=True)
    async def dank(self, ctx):
        """
        HuskieBot shitposts an image from its library

        Parameters
        ----------
        ctx : discord.ext.commands.Context

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
                    index = int(args[0]) - 1
                else:
                    index = randint(0, len(images))

                if index >= 0 and index <= len(images):
                    await ctx.send(index + 1, file=discord.File(os.path.join(MEDIA_PATH, images[index])))
                else:
                    raise RuntimeError
            except (ValueError, RuntimeError, IndexError):
                await ctx.send('That is not a valid meme')

    @dank.command(name='count')
    async def dank_count(self, ctx):
        """HuskieBot will say how many memes it currently has"""
        images = sorted(os.listdir(MEDIA_PATH))
        await ctx.send(f"I have {len(images)} dank memes")
