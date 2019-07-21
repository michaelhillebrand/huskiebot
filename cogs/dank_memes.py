import logging
import os
import typing
from collections import namedtuple
from io import BytesIO
from random import randint
from tempfile import NamedTemporaryFile
from zipfile import ZipFile

import cv2
import discord
import math
import numpy
import requests
from PIL import Image, ImageOps, ImageEnhance
from discord.ext import commands

from cogs import MEDIA_PATH, STATIC_PATH
from cogs.base import BaseCog
from utils.download import download

FlarePosition = namedtuple('FlarePosition', ['x', 'y', 'size'])


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

    def _salt_and_pepper(self, image):
        """
        Salts and Peppers image (numpy array)

        https://stackoverflow.com/questions/22937589/how-to-add-noise-gaussian-salt-and-pepper-etc-to-image-in-python-with-opencv

        :param image: numpy.array
        :return numpy.array:
        """
        s_vs_p = 0.1
        amount = 0.025
        out = numpy.copy(image)
        # Salt mode
        num_salt = numpy.ceil(amount * image.size * s_vs_p)
        coords = [numpy.random.randint(0, i - 1, int(num_salt))
                  for i in image.shape]
        out[tuple(coords)] = 1

        # Pepper mode
        num_pepper = numpy.ceil(amount * image.size * (1. - s_vs_p))
        coords = [numpy.random.randint(0, i - 1, int(num_pepper))
                  for i in image.shape]
        out[tuple(coords)] = 0
        return out

    def _saturate(self, img):
        """
        frys an image

        :param img: PIL.Image
        :return PIL.Image:
        """
        flare_positions = []
        opencv_img = cv2.cvtColor(numpy.array(img), cv2.COLOR_RGB2GRAY)
        faces = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')\
            .detectMultiScale(opencv_img,
                              scaleFactor=1.3,
                              minNeighbors=5,
                              minSize=(30, 30),
                              flags=cv2.CASCADE_SCALE_IMAGE
                              )
        for (x, y, w, h) in faces:
            face_roi = opencv_img[y:y+h, x:x+w]  # Get region of interest (detected face)
            eyes = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml').detectMultiScale(face_roi)
            for (ex, ey, ew, eh) in eyes:
                eye_corner = (ex + ew / 2, ey + eh / 2)
                flare_size = eh if eh > ew else ew
                flare_size *= 4
                corners = [math.floor(x) for x in eye_corner]
                flare_positions.append(FlarePosition(*corners, flare_size))

        # Crush image to hell and back
        width, height = img.width, img.height
        img = img.resize((int(width ** .75), int(height ** .75)), resample=Image.LANCZOS)
        img = img.resize((int(width ** .88), int(height ** .88)), resample=Image.BILINEAR)
        img = img.resize((int(width ** .9), int(height ** .9)), resample=Image.BICUBIC)
        img = img.resize((width, height), resample=Image.BICUBIC)
        img = ImageOps.posterize(img, 4)

        # Generate colour overlay
        r = img.split()[0]
        r = ImageEnhance.Contrast(r).enhance(2.0)
        r = ImageEnhance.Brightness(r).enhance(1.5)

        r = ImageOps.colorize(r, (254, 0, 2), (255, 255, 15))

        # Overlay red and yellow onto main image and sharpen the hell out of it
        img = Image.blend(img, r, 0.75)
        img = ImageEnhance.Sharpness(img).enhance(100.0)

        # Apply flares on any detected eyes
        if flare_positions:
            flare_img = Image.open(STATIC_PATH + 'images/flare.png')
            for flare in flare_positions:
                flare_transformed = flare_img.copy().resize((flare.size,) * 2, resample=Image.BILINEAR)
                img.paste(flare_transformed, (flare.x, flare.y), flare_transformed)

        return img

    def _deep_fry(self, image):
        file = NamedTemporaryFile(suffix='.jpg')
        image = image.convert('RGB')
        image = self._saturate(image)
        nparray = numpy.asarray(image)
        nparray = self._salt_and_pepper(nparray)
        nparray = nparray.astype('uint8')
        image = Image.fromarray(nparray)
        image.save(file)
        return file

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

    @commands.command()
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
                    index = int(args[0])
                else:
                    index = randint(0, len(images) - 1)
                await ctx.send(index, file=discord.File(os.path.join(MEDIA_PATH, images[index])))
            except (ValueError, RuntimeError, IndexError):
                await ctx.send('That is not a valid meme')

    @commands.command()
    async def deepfry(self, ctx, index: typing.Optional[int]):
        """
        Deep frys an image

        Parameters
        ----------
        ctx : discord.ext.commands.Context
        index : int (optional)

        Returns
        -------
        Image
            Deep Fried Image
        """
        if ctx.message.attachments:
            async with ctx.message.channel.typing():
                for attachment in ctx.message.attachments:
                    response = requests.get(attachment.url)
                    if response.status_code == 200:
                        try:
                            file = self._deep_fry(Image.open(BytesIO(response.content)))
                        except OSError:
                            await ctx.message.channel.send('I can\'t deep fry that file')
                        else:
                            await ctx.message.channel.send(file=discord.File(file.name))
                    else:
                        await ctx.message.channel.send('I could not download your file')
        elif index is not None:
            try:
                if index:
                    raise IOError
                file = self._deep_fry(Image.open(MEDIA_PATH + '{}.jpg'.format(index)))
                await ctx.message.channel.send(file=discord.File(file.name))
            except IOError:
                await ctx.message.channel.send('That is not a valid index')
        else:
            await ctx.message.channel.send('There is nothing to deep fry')
