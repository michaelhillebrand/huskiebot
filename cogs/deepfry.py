"""A cog that provides a command to take an image and return a version that looks like it's been put in a deepfryer."""

from tempfile import NamedTemporaryFile

import requests

import discord
from discord.ext import commands
from PIL import Image, ImageOps, ImageEnhance

from cogs.base import BaseCog


class Colours:
    """Enum for colors used in the Deepfryer."""

    RED = (254, 0, 2)
    YELLOW = (255, 255, 15)


class Deepfry(BaseCog):
    """Provide a command that takes an image and returns a version that looks like it's been put in a deepfryer."""

    file_types = [
        'bmp',
        'gif',
        'jpg',
        'jpeg',
        'png'
    ]

    @commands.command()
    async def deepfry(self, ctx: discord.ext.commands.Context) -> None:
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
            if check_file_type(attachment.filename, self.file_types):
                with NamedTemporaryFile() as tmp_file:
                    img = fry_to_shits(attachment.url, tmp_file)
                    img.save(tmp_file.name, format='JPEG')
                    await ctx.send(
                        # Returns it with a name that ends in .jpg so Discord
                        # will preview it correctly
                        file=discord.File(tmp_file.name, 'deepfried.jpg')
                    )
            else:
                await ctx.send(content=f'How the fuck am I supposed to deepfry a {attachment.filename.split(".")[-1].upper()} filetype?')  # noqa # ignore line length since it's a single line string


def fry_to_shits(url: str, temp_file: NamedTemporaryFile) -> Image:
    """
    Download and deepfry the provided image.

    Parameters
    ----------
    url : str
        The URL to download the image from
    temp_file: NamedTemporaryFile
        A NamedTemporaryFile to store the image in while we work with it

    Returns
    -------
    Image
        a Pill Image object

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
    r = ImageOps.colorize(r, Colours.RED, Colours.YELLOW)
    img = Image.blend(img, r, 0.75)
    img = ImageEnhance.Sharpness(img).enhance(100.0)
    return img


def check_file_type(filename: str, file_types: list) -> bool:
    """
    Check if the file type is in the list of accepted file types.

    Parameters
    ----------
    filename : str
    file_types : list

    Returns
    -------
    Bool

    """
    return filename.split('.')[-1] in file_types
