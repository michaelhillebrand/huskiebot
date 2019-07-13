import random
from random import randint
import typing

from discord.ext import commands


class Quotes(commands.Cog):
    KOTH = [
        "What the hell kind of country is this where I can only hate a man if he's white?",
        "What? No, I sell propane!",
        "Soccer was invented by European ladies to keep them busy while their husbands did the cooking",
        "BWAAAAHH!",
        "I don’t have an anger problem, I have an idiot problem.",
        "Bobby, some things are like a tire fire, trying to put it out only makes it worse. You just gotta grab a "
        "beer and let it burn.",
        "With the joys of responsibility comes the burden of obligation",
        "Why would anyone do drugs when they could just mow a lawn?",
        "Now you listen to me, mister. I work for a livin', and I mean real work, not writin' down gobbledegook! I "
        "provide the people of this community with propane and propane accessories. Oh, when I think of all my hard "
        "earned tax dollars goin' ta pay a bunch of little twig-boy bureaucrats like you, it just makes me wanna ... "
        "oh ... oh God",
        "God dang it, Bobby!",
        "We of the Order of the Straight Arrow call upon the spirit Wematanye, protector of the sacred ground that "
        "brings us cool water to drink and energy-efficient clean-burning propane gas for all our sacred heating and "
        "cooking needs. Wematanye says, respect the earth! She's ours, by God, our taxes pay for Her. Also, "
        "it says here you gotta love all Her creatures. Let's see...oh, here we go: Though we walk through the valley "
        "of the shadow of death, you're gonna recommend us to the spirit in the sky, with liberty and justice for "
        "all. Wematanye is with you, and with Texas. Amen.",
        "I am the mack daddy of Heimlich County, I play it straight up, yo. You get the hell outta my 'hood!",
        "Dang it, I am sick and tired of everyone's asinine ideas about me. I'm not a redneck, and I'm not some "
        "Hollywood jerk. I'm something else entirely. I'm... I'm complicated!",
        "Firm but with a little give. Yup, these are medium-rare.",
        "You know whats not cool Bobby? Hell.",
        "Do I Look Like I Know What a JPEG is?",
        "I'm so tired of you South Texas Pig Jockeys comin' in here, wakin' me up to say \"How 'bout them Cowboys!\". "
        "Arlen stinks and Wichita Falls rules! And you know why? Cause in five minutes I can be in the Great State of "
        "Oklahoma! Go Sooners!",
        "This tornado's already registered a level two on the Fujisaki scale. A storm that strong will send an egg "
        "through a barn door - two barn doors if one of them's open",
        "I know what's wrong with it. It's a Ford. You know what they say Ford stands for, don't ya? It stands for "
        "'Fix it again, Tony'",
    ]
    SHOWS = {
        'koth': KOTH
    }

    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True)
    async def quote(self, ctx, show: typing.Optional[str] = None, index: typing.Optional[int] = None):
        """HuskieBot will say a quote from show"""
        if ctx.invoked_subcommand is None:
            if show:
                try:
                    show_quotes = self.SHOWS[show]
                except KeyError:
                    await ctx.send('That is not a valid show')
                    return
            else:
                show_quotes = self.SHOWS[random.choice(list(self.SHOWS))]
            if not index:
                index = randint(0, len(show_quotes) - 1)
            try:
                await ctx.send(show_quotes[index])
            except IndexError:
                await ctx.send('That is not a valid quote')
                return

    @quote.command(name='count')
    async def quote_count(self, ctx):
        """HuskieBot will say how many quotes it current has"""
        await ctx.send("I have {} quotes from {} shows".format(sum([len(quotes) for _, quotes in self.SHOWS.items()]),
                                                               len(list(self.SHOWS))))
