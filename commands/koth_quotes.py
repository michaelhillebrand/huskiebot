from random import randint
from commands.base import BaseCommand


class KOTHQuotes(BaseCommand):
    trigger = 'quote'
    description = 'HuskieBot will say a quote from the best show ever made King of the Hill'

    CHOICES = [
        "'What the hell kind of country is this where I can only hate a man if he's white?'",
        "'What? No, I sell propane!'",
        "'Soccer was invented by European ladies to keep them busy while their husbands did the cooking'",
        "'BWAAAAHH!'",
        "'I don’t have an anger problem, I have an idiot problem.'",
        "'Bobby, some things are like a tire fire, trying to put it out only makes it worse. You just gotta grab a beer and let it burn.'",
        "'With the joys of responsibility comes the burden of obligation'",
        "'Why would anyone do drugs when they could just mow a lawn?'",
        "'Now you listen to me, mister. I work for a livin', and I mean real work, not writin' down gobbledegook! I provide the people of this community with propane and propane accessories. Oh, when I think of all my hard earned tax dollars goin' ta pay a bunch of little twig-boy bureaucrats like you, it just makes me wanna ... oh ... oh God'",
        "'God dang it, Bobby!'"
        "' We of the Order of the Straight Arrow call upon the spirit Wematanye, protector of the sacred ground that brings us cool water to drink and energy-efficient clean-burning propane gas for all our sacred heating and cooking needs. Wematanye says, respect the earth! She's ours, by God, our taxes pay for Her. Also, it says here you gotta love all Her creatures. Let's see...oh, here we go: Though we walk through the valley of the shadow of death, you're gonna recommend us to the spirit in the sky, with liberty and justice for all. Wematanye is with you, and with Texas. Amen.'",
        "'I am the mack daddy of Heimlich County, I play it straight up, yo. You get the hell outta my 'hood!'",
        "'Dang it, I am sick and tired of everyone's asinine ideas about me. I'm not a redneck, and I'm not some Hollywood jerk. I'm something else entirely. I'm... I'm complicated!'",
        "'Firm but with a little give. Yup, these are medium-rare.'",
        "'You know whats not cool Bobby? Hell.'",
        "'Do I Look Like I Know What a JPEG is?'"
    ]

    async def command(self, message):
        """
        Command to say a quote from King of the Hill

        :param message: discord.Message
        :return str:
        """
        try:
            args = message.content.split(' ')[1:]

            if len(args) > 1:
                raise RuntimeError
            elif len(args) == 1:
                if args[0] == 'count':
                    await message.channel.send("I have {} quotes".format(len(self.CHOICES)))
                    return
                elif int(args[0]) <= 0:
                    raise RuntimeError
                else:
                    index = int(args[0]) - 1
            else:
                index = randint(0, len(self.CHOICES) - 1)
            await message.channel.send(self.CHOICES[index])
        except(ValueError, RuntimeError, IndexError):
            await message.channel.send('That is not a valid quote')
