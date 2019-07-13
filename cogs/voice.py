import discord
from discord.ext import commands

class Voice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def _get_current_voice_client(self, ctx):
        for vc in self.bot.voice_clients:
            if vc.guild == ctx.guild:
                return vc
        return None

    @commands.command()
    async def invitebot(self, ctx):
        """
        HuskieBot will join user's voice channel

        Parameters
        ----------
        message : discord.Message

        Returns
        -------
        None

        """
        if ctx.author.voice == None:
            await ctx.send('You are not in a voice channel')
        else:
            vc = self._get_current_voice_client(ctx)
            if vc:
                await vc.move_to(ctx.author.voice.channel)
            else:
                vc = await ctx.author.voice.channel.connect()
            # vc.play(FFmpegPCMAudio('/home/michael/i_am_here.mp3'))

    @invitebot.error
    async def on_invitebot_error(self, ctx, error):
        await ctx.send('Sorry, there was an error joining your voice channel')

    @commands.command()
    async def disconnectbot(self, ctx):
        """
        HuskieBot will disconnect from its voice channel

        Parameters
        ----------
        message : discord.Message

        Returns
        -------
        None

        """
        vc = self._get_current_voice_client(ctx)
        if not vc:
            await ctx.send('HuskieBot is not in a voice channel')
        else:
            await vc.disconnect()
