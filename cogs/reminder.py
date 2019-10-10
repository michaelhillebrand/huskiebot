import datetime
import logging
import re

import discord
from discord.ext import commands

from cogs.base import BaseCog


class Reminder(BaseCog):
    prefix = '^!remindme\s+'
    prefix_regex = re.compile(prefix)
    offset_regex = re.compile(prefix + '\d+\s+(minutes*|hours*|days*|weeks*|months*|years*)\s+".+"$',
                              flags=re.IGNORECASE)
    relative_regex = re.compile(prefix + 'next\s+(sunday|monday|tueday|wednesday|thursday|friday|saturday)'
                                         '(\s+at\s+\d{1,2}\s*(pm|am)*)*\s+".+"$', flags=re.IGNORECASE)
    end_regex = re.compile(prefix + '(eoy|eom|eod)\s+".+"$', flags=re.IGNORECASE)

    WEEKDAYS ={
        'sunday': 0,
        'monday': 1,
        'tuesday': 2,
        'wednesday': 3,
        'thursday': 4,
        'friday': 5,
        'saturday': 6,
    }

    @commands.command()
    async def remindme(self, ctx):
        """
        HuskieBot will remind user of something later

        Parameters
        ----------
        ctx : discord.ext.commands.Context

        Returns
        -------
        str
            Confirmation of reminder
        """
        m = ctx.message.clean_content
        try:
            if self.offset_regex.match(m):
                logging.info('Matched offset')
                match = self.prefix_regex.match(m)
                args = m[match.end():].split(' ')
                date_unit = f'{args[1]}s' if args[1][-1] != 's' else args[1]
                remind_time = ctx.message.created_at + datetime.timedelta(**{date_unit: int(args[0])})
                message = args[-1]
            elif self.relative_regex.match(m):
                logging.info('Matched relative')
                match = self.prefix_regex.match(m)
                args = m[match.end():].split(' ')
                offset = self.WEEKDAYS[args[1].lower()] - ctx.message.created_at.weekday()
                if offset <= 0:
                    offset = 7 + offset
                remind_time = ctx.message.created_at + datetime.timedelta(days=offset)
                if len(args) == 5:
                    if 'pm' in args[3]:
                        hour = int(args[3][:-2]) + 12
                    elif 'am' in args[3]:
                        hour = int(args[3][:-2])
                    else:
                        hour = int(args[3])
                    remind_time = remind_time.replace(hour=hour, minute=0, second=0)
                message = args[-1]
            elif self.end_regex.match(m):
                logging.info('Matched end')
                match = self.prefix_regex.match(m)
                args = m[match.end():].split(' ')
                if args[0] == 'eod':
                    remind_time = ctx.message.created_at.replace(hour=23, minute=50, second=0)
                if args[0] == 'eom':
                if args[0] == 'eoy':
                message = args[-1]
            else:
                logging.warning('Message did not match any patterns')
                await ctx.send('I did not understand that format')
                return
        except Exception as e:
            logging.error(e)
            await ctx.send('I could not process your request')
        else:
            remind_time = remind_time.replace(microsecond=0)
            link_datetime = str(remind_time).replace(' ', '+')
            embed = discord.Embed(description=f"{ctx.author.mention} I\'ll message you on "
                                              f"[{remind_time} UTC](https://www.wolframalpha.com/input/?"
                                              f"i={link_datetime}+UTC+To+Local+Time) to remind you of this.")
            await ctx.send(embed=embed)
            # await ctx.send(f"{ctx.author.mention} I'll message you at {remind_time} to remind you of this")
