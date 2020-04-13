import asyncio

import discord
from discord import Message, Embed
from discord.ext import commands
from discord.ext.commands import Context
from cogs.base import BaseCog

MAX = 10
MIN = 1


class Poll(BaseCog):

    @commands.command(pass_context=True)
    async def poll(self, ctx: Context, question: str, minutes: str, *options: str) -> None:
        """
        generates a poll. Consists of a question, the options to choose from and the number of minutes to keep
        the poll going

        Parameters
        ----------
        ctx : Context
        question : Str
        minutes : Str
        options : Str

        Returns
        -------
        None
        """
        if MIN >= len(options) or len(options) > MAX:
            await ctx.message.delete()
            await ctx.send(
                f"Number of options needs to be more than 1 and less than 10. Number of options given: {len(options)}.")
            return
        await ctx.message.delete()
        reactions = generate_reactions(options)
        description = generate_poll_description(options, reactions)
        description_as_string = description_to_string(description)
        embed = generate_embed(question, description_as_string)
        poll_message = await ctx.send(embed=embed)
        await add_reactions_to_the_poll_message(poll_message, reactions, len(options))
        await asyncio.sleep(int(minutes) * 60)
        await ctx.send(embed=await generate_results(ctx, poll_message))


def generate_reactions(options: str) -> list:
    """
    generates a list of reactions depending on the number of options provided

    Parameters
    ----------
    options : list

    Returns
    -------
    List
        list of reactions
    """
    if len(options) == 2 and options[0].lower() == 'yes' and options[1].lower() == 'no':
        return ['\u2705', '\u274C']
    else:
        return ['1⃣', '2⃣', '3⃣', '4⃣', '5⃣', '6⃣', '7⃣', '8⃣', '9⃣', '🔟']


def generate_poll_description(options: str, reactions: list) -> dict:
    """
    generates description for the body of the poll

    Parameters
    ----------
    options : list
    reactions : list

    Returns
    -------
    Dict
        dictionary consisting of emoji + response as keys and number of those responses as values
    """
    description = {}
    for x, option in enumerate(options):
        description[f"{reactions[x]} {option}"] = 0
    return description


def string_description_to_dictionary(description: str) -> dict:
    """
    converts a description string to a dictionary

    Parameters
    ----------
    description : Str

    Returns
    -------
    Dict
        description as a dictionary
    """
    return dict((x.strip(), y.strip()) for x, y in (element.split('-') for element in description.split('\n')))


def description_to_string(description: dict) -> str:
    """
    converts a description dictionary to a string

    Parameters
    ----------
    description : Dict

    Returns
    -------
    Str
        description as a string
    """
    description_string = ''
    for element in description:
        description_string += f"{element} - {description[element]}\n"
    return description_string


async def add_reactions_to_the_poll_message(message: Message, reactions: list, number_of_options: int) -> None:
    """
    adds reactions to chose from to the poll message

    Parameters
    ----------
    message : Message
    reactions : list
    number_of_options : int

    Returns
    -------
    None
    """
    for reaction in reactions[:number_of_options]:
        await message.add_reaction(reaction)


def get_new_description(description: dict, reactions: list) -> str:
    """
    iterates over reactions and creates a new description with the new count of reactions

    Parameters
    ----------
    description : dict
    reactions : list

    Returns
    -------
    Str
        new description
    """
    new_description = ''
    x = 0
    for element in description:
        new_description += f'{element} - {reactions[x].count - 1 if len(reactions) > x else 0}\n'
        x += 1
    return new_description


def generate_embed(question: str, description: str) -> Embed:
    """
    generates an embed for the poll

    Parameters
    ----------
    question : str
    description : str

    Returns
    -------
    Embed
        embed for the poll
    """
    embed = discord.Embed(title=question, description=description, colour=discord.Color.orange())
    embed.set_footer(text='Poll')
    return embed


async def generate_results(ctx: Context, poll_message: Message) -> Embed:
    """
    generates embed with the results of the poll

    Parameters
    ----------
    ctx : Context
    poll_message : Message

    Returns
    -------
    Embed
       embed with the results of the poll
    """
    new_message = await ctx.fetch_message(poll_message.id)
    await new_message.edit(embed=new_message.embeds[0].set_footer(text=''))
    embed = discord.Embed(title=f'Results of the poll({new_message.embeds[0].title})',
                          description=new_message.embeds[0].description)
    return embed
