import datetime
import logging
import pickle
import os
from random import randint

import discord
from PIL import Image
from discord.ext import commands, tasks

from cogs import MEDIA_PATH, BASE_PATH
from cogs.base import BaseCog
from utils.download import download


class DankMemes(BaseCog):

    def __init__(self, bot) -> None:
        self.channel_id = int(os.getenv('MEME_CHANNEL'))
        self.channel = None
        self.last_fetch = None
        try:
            with open(f'{BASE_PATH}/last_scrape.pkl', 'rb') as f:
                self.last_fetch = pickle.load(f)
        except Exception:
            pass
        if self.channel_id:
            self.dank_meme_uploader.start()
        else:
            logging.warning('No channel ID was provided')
        super().__init__(bot)

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
        next_index = len(os.listdir(MEDIA_PATH)) + 1
        if image.format == 'GIF':
            image.save(os.path.join(MEDIA_PATH, f'{next_index}.gif'),
                       save_all=True,
                       optimize=True
                       )
        else:
            image = image.convert(mode='RGB')
            image.save(os.path.join(MEDIA_PATH, f'{next_index}.jpg'),
                       format='JPEG',
                       optimize=True
                       )

    def cog_unload(self):
        self.dank_meme_uploader.cancel()

    @tasks.loop(hours=6)
    async def dank_meme_uploader(self):
        """
        HuskieBot will scrap all new memes from the mods are asleep board and upload them

        Returns
        -------
            discord.Activity
        """
        logging.info("uploading dank memes")
        successful_uploads = 0
        failed_uploads = 0
        # while True:
        #     messages = await self.channel.history(limit=100, after=self.last_fetch, oldest_first=True).flatten()
        #     logging.debug(f'messages found: {len(messages)}')
        #     if len(messages) == 0:
        #         break
        #     self.last_fetch = messages[-1].created_at
        #     for message in messages:
        #         for attachment in message.attachments:
        #             file = await download(attachment.url)
        #             try:
        #                 await self._process_image(file)
        #                 successful_uploads += 1
        #             except Exception:
        #                 logging.warning('attachment was not an valid image')
        #                 failed_uploads += 1
        #     with open(f'{BASE_PATH}/last_scrape.pkl', 'wb') as f:
        #         pickle.dump(self.last_fetch, f)
        # logging.debug(f'{successful_uploads} files successfully uploaded')
        # logging.debug(f'{failed_uploads} files failed to upload')
        # if successful_uploads > 0:
        #     await self.channel.send(f'{successful_uploads} dank meme(s) uploaded')

    @dank_meme_uploader.before_loop
    async def before_dank_meme_uploader(self):
        await self.bot.wait_until_ready()
        channel = self.bot.get_channel(self.channel_id)
        if channel:
            self.channel = channel
        else:
            logging.error('Channel ID was invalid')
            raise ValueError

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
        if ctx.invoked_subcommand is None:
            images = os.listdir(MEDIA_PATH)
            current_index = len(images)
            if current_index == 0:
                await ctx.send("I don't have any images to shitpost with")
            else:
                try:
                    args = ctx.message.content.split(' ')[1:]
                    if len(args) > 1:
                        raise RuntimeError
                    elif len(args) == 1:
                        index = int(args[0])
                    else:
                        index = randint(1, current_index)

                    if index and index <= current_index:
                        await ctx.send(index, file=discord.File(os.path.join(MEDIA_PATH, f'{index}.jpg')))
                    else:
                        raise RuntimeError
                except (ValueError, RuntimeError, IndexError):
                    await ctx.send('That is not a valid meme')

    @dank.command(name='count')
    async def dank_count(self, ctx):
        """HuskieBot will say how many memes it currently has"""
        await ctx.send(f"I have {len(os.listdir(MEDIA_PATH))} dank memes")
