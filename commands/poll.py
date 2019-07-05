import discord

from commands.base import BaseCommand


class Poll(BaseCommand):
    trigger = 'poll'
    description = 'HuskieBot will generate a poll and display results'

    SECONDS = 'seconds'
    MINUTES = 'minutes'
    HOURS = 'hours'
    DAYS = 'days'

    MODES = {
        's': SECONDS,
        'm': MINUTES,
        'h': HOURS,
        'd': DAYS
    }

    DEFAULT_TIME_SECONDS = 60
    MAX_TIME_SECONDS = 60
    DEFAULT_TIME_MINUTES = 30
    MAX_TIME_MINUTES = 60
    DEFAULT_TIME_HOURS = 12
    MAX_TIME_HOURS = 24
    DEFAULT_TIME_DAYS = 1
    MAX_TIME_DAYS = 7

    async def command(self, message):
        """
        HuskieBot will generate a poll and display results

        :param message: discord.Message
        :return :
        """
        args = message.content.split(' ')[1:]
        try:
            if args[0][0] == '-':
                try:
                    mode = self.MODES[args[0][1]]
                    time = int(args[1])
                    args.pop(0)
                    args.pop(1)
                except (IndexError, ValueError):
                    await message.channel.send('That is not a valid time')
            else:
                mode = self.SECONDS
                time = self.DEFAULT_TIME_SECONDS

            # if len(options) <= 1:
            #     await self.bot.say('You need more than one option to make a poll!')
            #     return
            # if len(options) > 10:
            #     await self.bot.say('You cannot make a poll for more than 10 things!')
            #     return
            #
            # if len(options) == 2 and options[0] == 'yes' and options[1] == 'no':
            #     reactions = ['✅', '❌']
            # else:
            #     reactions = ['1⃣', '2⃣', '3⃣', '4⃣', '5⃣', '6⃣', '7⃣', '8⃣', '9⃣', '🔟']
            #
            # description = []
            # for x, option in enumerate(options):
            #     description += '\n {} {}'.format(reactions[x], option)
            # embed = discord.Embed(title=question, description=''.join(description))
            # react_message = await self.bot.say(embed=embed)
            # for reaction in reactions[:len(options)]:
            #     await self.bot.add_reaction(react_message, reaction)
            # embed.set_footer(text='Poll ID: {}'.format(react_message.id))
            # await self.bot.edit_message(react_message, embed=embed)
        except Exception as e:
            print(e)
