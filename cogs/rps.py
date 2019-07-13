import math
from random import randint

import discord
from discord.ext import commands

from cogs.base import BaseCog


class RockPaperScissors(BaseCog):
    stats = {}

    ROCK = 'rock'
    PAPER = 'paper'
    SCISSORS = 'scissors'

    CHOICES = [ROCK, PAPER, SCISSORS]

    async def _play(self, ctx, move):
        if self.stats.get(ctx.author.id, None):
            bot_move = self.CHOICES[randint(0, len(self.CHOICES) - 1)]
            if bot_move == move:
                result = 0
            elif (bot_move == self.ROCK and move == self.PAPER) or \
                    (bot_move == self.PAPER and move == self.SCISSORS) or \
                    (bot_move == self.SCISSORS and move == self.ROCK):
                result = 1
            elif (bot_move == self.ROCK and move == self.SCISSORS) or \
                    (bot_move == self.PAPER and move == self.ROCK) or \
                    (bot_move == self.SCISSORS and move == self.PAPER):
                result = -1
            else:
                result = -2
            game = self.stats[ctx.author.id]
            game['turn'] += 1
            game['history'].append({'bot': bot_move, 'user': move, 'result': result})
            if result == 1:
                game['user_score'] += 1
            elif result == -1:
                game['bot_score'] += 1
            elif result == 0:
                game['ties'] += 1
            # TODO: Consider how to improve this in cases of even number for best_of. Right now, with a best_of = 4, the game ends if one side gets to 2 wins, even if there are stil 2 turns left so thee's a possibility of a tie
            if max(game['user_score'], game['bot_score']) >= math.ceil(game['best_of'] / 2):
                await ctx.send('{user}\t\t\tHuskieBot\n'
                                           '{user_move}\tvs.\t{bot_move}\n'
                                           'GAME OVER\n'
                                           'Final Score: {user_score}-{bot_score}-{ties}\n\n'
                                           'Want to play again?'
                                           .format(user=ctx.author.mention,
                                                   user_move=move.capitalize(),
                                                   bot_move=bot_move.capitalize(),
                                                   user_score=game['user_score'],
                                                   bot_score=game['bot_score'],
                                                   ties=game['ties']
                                                   )
                                           )
                self.stats.pop(ctx.author.id, None)
            else:
                await ctx.send('{user}\t\t\tHuskieBot\n'
                                           '{user_move}\tvs.\t{bot_move}\n'
                                           'Current Score: {user_score}-{bot_score}-{ties}'
                                           .format(user=ctx.author.mention,
                                                   user_move=move.capitalize(),
                                                   bot_move=bot_move.capitalize(),
                                                   user_score=game['user_score'],
                                                   bot_score=game['bot_score'],
                                                   ties=game['ties']
                                                   )
                                           )

    def _initialize(self, ctx, best_of):
        self.stats.update({ctx.author.id: {
            'turn': 1,
            'history': [],
            'user_score': 0,
            'bot_score': 0,
            'ties': 0,
            'best_of': best_of,
        }})

    @commands.command()
    async def rps(self, ctx):
        """
        HuskieBot will play a game of ROCK, PAPER, Scissors with user

        Parameters
        ----------
        message : discord.Message

        Returns
        -------
        str

        """
        args = ctx.message.content.split(' ')[1:]
        if len(args) == 0:
            if self.stats.get(ctx.author.id, None):
                game = self.stats[ctx.author.id]
                await ctx.send(
                    'I already have a game started with you.\n'
                    'We are on turn {} with a best of {}.\n'
                    'The current score is {}-{}-{}'.format(game['turn'],
                                                           game['best_of'],
                                                           game['user_score'],
                                                           game['bot_score'],
                                                           game['ties']))
            else:
                self._initialize(ctx, 3)
                await ctx.send('Lets play! Send me a move. (!rps rock, !rps paper, !rps scissors)')
        elif len(args) == 1:
            try:
                self._initialize(ctx, int(args[-1]))
                await ctx.send('Lets play! Send me a move. (!rps rock, !rps paper, !rps scissors)')
            except ValueError:
                if not self.stats.get(ctx.author.id, None):
                    await ctx.send('We don\'t have a game going. '
                                               'Start a game by using the !{} command'.format(ctx.command))
                else:
                    if args[-1].lower() in self.CHOICES:
                        await self._play(ctx, args[-1].lower())
                    else:
                        await ctx.send('That is not a valid move')

        else:
            await ctx.send('That is not a valid argument')
