import logging

from discord.ext import commands

from cogs.base import BaseCog


class Voice(BaseCog):

    def _get_current_voice_client(self, ctx: commands.Context):
        """Retreives bot's current client (if any)."""
        for vc in ctx.bot.voice_clients:
            if vc.guild == ctx.guild:
                return vc
        return None

    @commands.command()
    async def invite_bot(self, ctx: commands.Context):
        """
        HuskieBot will join user's voice channel

        Parameters
        ----------
        ctx : discord.ext.commands.Context

        Returns
        -------
        None

        """
        if ctx.author.voice is None:
            await ctx.send('You are not in a voice channel')
        else:
            vc = self._get_current_voice_client(ctx)
            if vc:
                await vc.move_to(ctx.author.voice.channel)
            else:
                vc = await ctx.author.voice.channel.connect()
            # vc.play(FFmpegPCMAudio('/home/michael/i_am_here.mp3'))

    @invite_bot.error
    async def on_invitebot_error(self, ctx: commands.Context, error: commands.CommandInvokeError):
        logging.error(error)
        await ctx.send('Sorry, there was an error joining your voice channel')

    @commands.command()
    async def disconnect_bot(self, ctx: commands.Context):
        """
        HuskieBot will disconnect from its voice channel

        Parameters
        ----------
        ctx : discord.ext.commands.Context

        Returns
        -------
        None

        """
        vc = self._get_current_voice_client(ctx)
        if not vc:
            await ctx.send('HuskieBot is not in a voice channel')
        else:
            await vc.disconnect()
