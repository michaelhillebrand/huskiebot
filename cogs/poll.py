import asyncio
import discord
from discord.ext import commands
from cogs.base import BaseCog


class Poll(BaseCog):

    @commands.command(pass_context=True)
    async def poll(self, ctx, question, minutes, *options: str):
        """ Generates a poll. Consists of a question, the options to choose from and the number of minutes to keep
        the poll going

        :param ctx: Context of the command message
        :param question: Question for the poll
        :param options: List of options to choose from
        :param minutes: Number of minutes to run the poll for
        :return: None
        """
        if number_of_options_does_not_fall_in_range(options):
            await ctx.send('Number of options needs to be more than 1 and less than 10. Number of options given: {}.'
                           .format(len(options)))
            return
        await ctx.message.delete()
        reactions = generate_reactions(options)
        description = generate_poll_description(options, reactions)
        description_as_string = description_to_string(description)
        embed = discord.Embed(title=question, description=description_as_string, colour=discord.Color.orange())
        embed.set_footer(text='Poll:')
        poll_message = await ctx.send(embed=embed)
        await add_reactions_to_the_poll_message(poll_message, reactions, len(options))
        await asyncio.sleep(int(minutes) * 60)
        await ctx.send(embed=await generate_results(ctx, poll_message))


def number_of_options_does_not_fall_in_range(options) -> bool:
    """Checks if the number of options provided falls into the range between 2 and 10.

    :param options: list of options
    :return: True or False
    """
    return 1 >= len(options) > 10


def generate_reactions(options) -> list:
    """ Generates a list of reactions depending on the number of options provided

    :param options: list of options.
    :return: list of reactions
    """
    if len(options) == 2 and options[0] == 'yes' and options[1] == 'no':
        return ['✅', '❌']
    else:
        return ['1⃣', '2⃣', '3⃣', '4⃣', '5⃣', '6⃣', '7⃣', '8⃣', '9⃣', '🔟']


def generate_poll_description(options, reactions) -> dict:
    """ Generates description for the body of the poll

    :param options: choices a user can pick from
    :param reactions: list emojis to use as responses
    :return: a list consisting of emoji + response strings
    """

    description = {}
    for x, option in enumerate(options):
        description["{} {}".format(reactions[x], option)] = 0
    return description


def string_description_to_dictionary(description) -> dict:
    """ Converts a description string to a dictionary

    :param description: dictionary
    :return: description sting
    """
    return dict((x.strip(), y.strip()) for x, y in (element.split('-') for element in description.split('\n')))


def description_to_string(description) -> str:
    """ Converts a description dictionary to a string

    :param description: dictionary
    :return: description string
    """
    description_string = ''
    for element in description:
        description_string += "{} - {}\n".format(element, description[element])
    return description_string


async def add_reactions_to_the_poll_message(message, reactions, number_of_options) -> None:
    """ Adds reactions to chose from to the poll message

    :param message: message to add reactions to
    :param reactions: list of reactions/emojis
    :param number_of_options: number of options provided
    :return: None
    """
    for reaction in reactions[:number_of_options]:
        await message.add_reaction(reaction)


def get_new_description(description, reactions) -> str:
    """ Iterates over reactions and creates a new description with the new count of reactions

    :param description: description of the embed
    :param reactions: list of reactions
    :return: new description
    """
    new_description = ''
    x = 0
    for element in description:
        new_description += '{} - {}\n'.format(element, reactions[x].count - 1 if len(reactions) > x else 0)
        x += 1
    return new_description


async def generate_results(ctx, poll_message):
    """ Generates embed with the results of the poll

    :param ctx: context of the poll
    :param poll_message: message containing the poll
    :return: embed with the results of the poll
    """
    new_message = await ctx.fetch_message(poll_message.id)
    await new_message.edit(embed=new_message.embeds[0].set_footer(text=''))

    embed = discord.Embed(title='Results of the poll({})'.format(new_message.embeds[0].title),
                          description=new_message.embeds[0].description)
    return embed
