from collections import namedtuple
from io import BytesIO
from tempfile import NamedTemporaryFile

import cv2
import discord
import math
import numpy
import numpy as np
import requests
from PIL import Image, ImageOps, ImageEnhance

from commands.base import BaseCommand
from discord_bot import STATIC_PATH, MEDIA_PATH

FlarePosition = namedtuple('FlarePosition', ['x', 'y', 'size'])


class DeepFry(BaseCommand):
    trigger = 'deepfry'
    description = 'Deep frys an image'

    def salt_and_pepper(self, image):
        """
        Salts and Peppers image (numpy array)

        :param image: numpy.array
        :return numpy.array:
        """
        s_vs_p = 0.1
        amount = 0.025
        out = np.copy(image)
        # Salt mode
        num_salt = np.ceil(amount * image.size * s_vs_p)
        coords = [np.random.randint(0, i - 1, int(num_salt))
                  for i in image.shape]
        out[tuple(coords)] = 1

        # Pepper mode
        num_pepper = np.ceil(amount * image.size * (1. - s_vs_p))
        coords = [np.random.randint(0, i - 1, int(num_pepper))
                  for i in image.shape]
        out[tuple(coords)] = 0
        return out

    def fry(self, img, flares=False):
        """
        frys an image

        :param img: PIL.Image
        :param flares: bool
        :return PIL.Image:
        """
        flare_positions = []
        if flares:
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

    def process_image(self, image, flares=False):
        file = NamedTemporaryFile(suffix='.jpg')
        Image.fromarray(self.salt_and_pepper(np.asarray(self.fry(image.convert('RGB'), flares=flares))).astype('uint8')).save(file)
        return file

    async def command(self, message):
        """
        Deep frys an image

        :param message: discord.Message
        :return discord.File:
        """
        flares = False
        args = message.content.split(' ')[1:]
        if any(arg in ['-f', '--flares'] for arg in args):
            flares = True
            args.remove('-f')
        if message.attachments:
            async with message.channel.typing():
                for attachment in message.attachments:
                    response = requests.get(attachment.url)
                    if response.status_code == 200:
                        file = self.process_image(Image.open(BytesIO(response.content)), flares=flares)
                    await message.channel.send(file=discord.File(file.name))
        elif args == 1:
            try:
                file = self.process_image(Image.open(MEDIA_PATH, '/{}.jpg'.format(args[0])), flares=flares)
                await message.channel.send(file=discord.File(file.name))
            except IOError:
                await message.channel.send('That is not a valid meme index number')
        else:
            await message.channel.send('There is nothing to deep fry')
