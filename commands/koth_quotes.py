from commands.base import BaseCommand
from random import randint

class KOTHQuotes(BaseCommand):
    trigger = 'quote'
    description = 'HuskieBot will say a quote from the best show ever made King of the Hill'

    CHOICES = [
        "\"What the hell kind of country is this where I can only hate a man if he's white?\"",
        "\"What? No, I sell propane!\"",
        "\"Soccer was invented by European ladies to keep them busy while their husbands did the cooking\"",
        "\"BWAAAAHH!\"",
        "\"I don’t have an anger problem, I have an idiot problem.\"",
        "\"Bobby, some things are like a tire fire, trying to put it out only makes it worse. You just gotta grab a beer and let it burn.\"",
        "\"With the joys of responsibility comes the burden of obligation\"",
        "\"Why would anyone do drugs when they could just mow a lawn?\"",
        "\"Now you listen to me, mister. I work for a livin', and I mean real work, not writin' down gobbledegook! I provide the people of this community with propane and propane accessories. Oh, when I think of all my hard earned tax dollars goin' ta pay a bunch of little twig-boy bureaucrats like you, it just makes me wanna ... oh ... oh God\"",
        "\"God dang it, Bobby!\""
    ]

    async def command(self, message):
        """
        Command to say a quote from King of the Hill

        :param message: discord.Message
        :return str:
        """
        await message.channel.send(self.CHOICES[randint(0, len(self.CHOICES) - 1)])