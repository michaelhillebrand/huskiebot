from discord.ext.commands import DefaultHelpCommand


class HuskieBotHelpCommand(DefaultHelpCommand):

    def __init__(self, **options):
        super().__init__(dm_help=True, **options)

    async def command_callback(self, ctx, *, command=None):
        await ctx.message.delete()
        return await super().command_callback(ctx, command=command)
