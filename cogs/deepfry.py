import os
from tempfile import TemporaryFile

import requests

import discord
from discord.ext import commands
from PIL import Image, ImageOps, ImageEnhance

from cogs.base import BaseCog


class Colours:
    RED = (254, 0, 2)
    YELLOW = (255, 255, 15)


class Deepfry(BaseCog):
    file_types = [
        'bmp',
        'gif',
        'jpg',
        'jpeg',
        'png'
    ]

    @commands.command()
    async def deepfry(self, ctx):
        for attachment in ctx.message.attachments:
            if check_file_type(attachment.filename, self.file_types):
                img = fry_to_shits(attachment.url)
                img.save('deepfry.jpg')
                await ctx.send(file=discord.File('deepfry.jpg'))
                os.remove('deepfry.jpg')
            else:
                await ctx.send(content=f'How the fuck am I supposed to deepfry a {attachment.filename.split(".")[-1].upper()} filetype?')


def fry_to_shits(url: str) -> Image:
    """
    downloads and deepfries the image

    Parameters
    ----------
    url : str

    Returns
    -------
    Image
        a Pill Image object
    """
    response = requests.get(url)
    temp_file = TemporaryFile()
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
    checks if the file type is in the list of accepted file types
    Parameters
    ----------
    filename : str
    file_types : list

    Returns
    -------
    Bool
    """
    return filename.split('.')[-1] in file_types
