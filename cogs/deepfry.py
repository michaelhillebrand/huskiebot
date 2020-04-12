from io import BytesIO
import discord
import requests
from PIL import Image, ImageOps, ImageEnhance
from discord.ext import commands
from cogs.base import BaseCog

FILE_TYPES = [
    'bmp',
    'gif',
    'jpg',
    'jpeg',
    'png'
]


class Colours:
    RED = (254, 0, 2)
    YELLOW = (255, 255, 15)


class Deepfry(BaseCog):
    @commands.command()
    async def deepfry(self, ctx):
        for attachment in ctx.message.attachments:
            if check_file_type(attachment.filename):
                img = fry_to_shits(attachment.url)
                img.save('deepfry.jpg')
                await ctx.send(file=discord.File('deepfry.jpg'))
            else:
                await ctx.send(content='How the fuck am I supposed to deepfry a {} filetype?'
                               .format(attachment.filename.split('.')[-1].upper()))


def fry_to_shits(url) -> Image:
    """ Downloads and deepfries the image

    :param url: image url
    :return: Image object
    """
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
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


def check_file_type(filename) -> bool:
    """ Checks if the file type is in the list of accepted file types

    :param filename: name of the file from Discord
    :return: True or False
    """
    return filename.split('.')[-1] in FILE_TYPES
