import asyncio
from time import strftime, gmtime

import discord
import typing
from discord.ext import commands

from cogs.base import BaseCog


class Poll(BaseCog):
    DEFAULT_TIME_SECONDS = 60
    MAX_TIME_SECONDS = 60480
    SECONDS = 'seconds'
    MINUTES = 'minutes'
    HOURS = 'hours'
    DAYS = 'days'

    MODES = {
        's': 1,
        'm': 60,
        'h': 360,
        'd': 8640
    }

    reactions = [
        "\N{REGIONAL INDICATOR SYMBOL LETTER A}",
        "\N{REGIONAL INDICATOR SYMBOL LETTER B}",
        "\N{REGIONAL INDICATOR SYMBOL LETTER C}",
        "\N{REGIONAL INDICATOR SYMBOL LETTER D}",
        "\N{REGIONAL INDICATOR SYMBOL LETTER E}",
        "\N{REGIONAL INDICATOR SYMBOL LETTER F}",
        "\N{REGIONAL INDICATOR SYMBOL LETTER G}",
        "\N{REGIONAL INDICATOR SYMBOL LETTER H}",
        "\N{REGIONAL INDICATOR SYMBOL LETTER I}",
        "\N{REGIONAL INDICATOR SYMBOL LETTER J}",
        "\N{REGIONAL INDICATOR SYMBOL LETTER K}",
        "\N{REGIONAL INDICATOR SYMBOL LETTER L}",
        "\N{REGIONAL INDICATOR SYMBOL LETTER M}",
        "\N{REGIONAL INDICATOR SYMBOL LETTER N}",
        "\N{REGIONAL INDICATOR SYMBOL LETTER O}",
        "\N{REGIONAL INDICATOR SYMBOL LETTER P}",
        "\N{REGIONAL INDICATOR SYMBOL LETTER Q}",
        "\N{REGIONAL INDICATOR SYMBOL LETTER R}",
        "\N{REGIONAL INDICATOR SYMBOL LETTER S}",
        "\N{REGIONAL INDICATOR SYMBOL LETTER T}",
        "\N{REGIONAL INDICATOR SYMBOL LETTER U}",
        "\N{REGIONAL INDICATOR SYMBOL LETTER V}",
        "\N{REGIONAL INDICATOR SYMBOL LETTER W}",
        "\N{REGIONAL INDICATOR SYMBOL LETTER X}",
        "\N{REGIONAL INDICATOR SYMBOL LETTER Y}",
        "\N{REGIONAL INDICATOR SYMBOL LETTER Z}"
    ]

    @commands.command()
    async def poll(self, ctx, question: str, answers: list, time : typing.Optional[int] = 60):
        """
        HuskieBot will generate a poll and display results

        Parameters
        ----------
        ctx
        question
        answers
        time

        Returns
        -------
        discord.Embed
            The generated poll
        """
        # if args[0][0] == '-':
        #     try:
        #         time = int(args[1]) * self.MODES[args[0][1]]
        #         if time <= 0 or time > self.MAX_TIME_SECONDS:
        #             raise ValueError
        #     except (IndexError, ValueError):
        #         await ctx.send('That is not a valid time')
        #         return
        # else:
        #     time = self.DEFAULT_TIME_SECONDS
        #
        # first = message.content.find("[")
        # last = message.content.find("]")
        # if first == -1 or last == -1:
        #     await message.channel.send('No options were given')
        #     return
        # options = message.content[first + 1:last].split(',')
        # if len(options) <= 1 or len(options) > 26:
        #     await message.channel.send('You must have at least have between 2-26 options')
        #     return
        # question = message.content[:first + 1]
        # description = '\n'.join('{} {}'.format(self.reactions[x], option.strip()) for x, option in enumerate(options))
        # embed = discord.Embed(title=question, description=description)
        # poll = await ctx.send(embed=embed)
        # for reaction in self.reactions[:len(options)]:
        #     await poll.add_reaction(reaction)
        #
        # # Wait for poll to be done
        # while True:
        #     if time <= 0:
        #         break
        #     elif time <= 60:
        #         sleep = 1
        #     elif time <= 360:
        #         sleep = 60
        #     elif time <= 8640:
        #         sleep = 360
        #     else:
        #         sleep = 8640
        #     await asyncio.sleep(sleep)
        #     time -= sleep
        #     embed.set_footer(text='Time Left: {}'.format(strftime('%H:%M:%S', gmtime(time))))
        #     await poll.edit(embed=embed)
        #
        # # Display results
        # poll = await ctx.fetch_message(poll.id)
        # results = [reaction.count - 1 for reaction in poll.reactions[:len(options)]]
        # total_answers = sum(results)
        # if total_answers:
        #     embed.description += '\n\n' + '\n'.join('{}  {}%'.format('|' * int(result / total_answers * 100), int(result / total_answers * 100)) for result in results)
        # else:
        #     embed.description += '\n\n' + 'There are no results to display'
        # embed.title += ' (closed)'
        # embed.set_footer()
        #
        # # description += '\n' + '\n'.join('' for )
        # await poll.edit(embed=embed)
        await ctx.send('pong')

    @poll.error
    async def on_poll_error(self, ctx, error):
        """
        Handles error from poll command

        Parameters
        ----------
        ctx : discord.ext.commands.Context
        error : Error

        Returns
        -------
            str
        """
        await ctx.send('Invalid arguments were passed')
