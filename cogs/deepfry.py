"""A cog that provides a command to take an image and return a version that looks like it's been put in a deepfryer."""
from enum import Enum
from tempfile import NamedTemporaryFile

import discord
from discord.ext import commands
from PIL import Image, ImageOps, ImageEnhance
import requests

from cogs.base import BaseCog


class Colors(Enum):
    """Enum for colors used in the Deep fryer."""

    RED = (254, 0, 2)
    YELLOW = (255, 255, 15)


class Deepfry(BaseCog):
    """Provide a command that takes an image and returns a version that looks like it's been put in a deep fryer."""

    file_types = [
        'bmp',
        'gif',
        'jpg',
        'jpeg',
        'png'
    ]

    @classmethod
    def _fry_to_shits(cls, url: str, temp_file: NamedTemporaryFile) -> Image:
        """
        Download and deep fry the provided image.

        Parameters
        ----------
        url : str
            The URL to download the image from
        temp_file: NamedTemporaryFile
            A NamedTemporaryFile to store the image in while we work with it

        Returns
        -------
        Image
            a PIL Image object

        """
        response = requests.get(url)
        temp_file.write(response.content)
        img = Image.open(temp_file)
        img = img.convert('RGB')
        width, height = img.width, img.height
        img = img.resize((int(width ** .75), int(height ** .75)), resample=Image.LANCZOS)
        img = img.resize((int(width ** .88), int(height ** .88)), resample=Image.BILINEAR)
        img = img.resize((int(width ** .9), int(height ** .9)), resample=Image.BICUBIC)
        img = img.resize((width, height), resample=Image.BICUBIC)
        img = ImageOps.posterize(img, 4)
        r = img.split()[0]
        r = ImageEnhance.Contrast(r).enhance(2.0)
        r = ImageEnhance.Brightness(r).enhance(1.5)
        r = ImageOps.colorize(r, Colors.RED, Colors.YELLOW)
        img = Image.blend(img, r, 0.75)
        img = ImageEnhance.Sharpness(img).enhance(100.0)
        return img

    @commands.command()
    async def deepfry(self, ctx: discord.ext.commands.Context):
        """
        Take an attached image, deep fry it, then return the results.

        Parameters
        ----------
        ctx : discord.ext.commands.Context

        Returns
        -------
        discord.File
            Dank Image

        """
        for attachment in ctx.message.attachments:
            filename = attachment.filename.split('.')[-1]
            if filename in self.file_types:
                with NamedTemporaryFile() as tmp_file:
                    img = self._fry_to_shits(attachment.url, tmp_file)
                    img.save(tmp_file.name, format='JPEG')
                    await ctx.send(file=discord.File(tmp_file.name, f'deep_fried_{filename}.jpg'))
            else:
                await ctx.send(content=f'How the fuck am I supposed to deepfry a {filename.upper()} filetype?')  # noqa # ignore line length since it's a single line string
