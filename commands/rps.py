from random import randint

import math

from commands.base import BaseCommand


class RockPaperScissors(BaseCommand):
    trigger = 'rps'
    description = 'Starts a Rock, Paper, Scissors game with HuskieBot'

    stats = {}

    ROCK = 'rock'
    PAPER = 'paper'
    SCISSORS = 'scissors'

    CHOICES = [ROCK, PAPER, SCISSORS]

    def __init__(self, client=None) -> None:
        self.will = None
        super().__init__(client)

    async def _play(self, message, move):
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
        game = self.stats[message.author.id]
        game['turn'] += 1
        game['history'].append({'bot': bot_move, 'user': move, 'result': result})
        if result == 1:
            game['user_score'] += 1
        elif result == -1:
            game['bot_score'] += 1
        elif result == 0:
            game['ties'] += 1
        if max(game['user_score'], game['bot_score']) >= math.ceil(game['best_of'] / 2):
            await message.channel.send('{user}\t\t\tHuskieBot\n'
                                       '{user_move}\tvs.\t{bot_move}\n'
                                       'GAME OVER\n'
                                       'Final Score: {user_score}-{bot_score}-{ties}\n\n'
                                       'Want to play again?'
                                       .format(user=message.author.mention,
                                               user_move=move.capitalize(),
                                               bot_move=bot_move.capitalize(),
                                               user_score=game['user_score'],
                                               bot_score=game['bot_score'],
                                               ties=game['ties']
                                               )
                                       )
            self.stats.pop(message.author.id, None)
        else:
            await message.channel.send('{user}\t\t\tHuskieBot\n'
                                       '{user_move}\tvs.\t{bot_move}\n'
                                       'Current Score: {user_score}-{bot_score}-{ties}'
                                       .format(user=message.author.mention,
                                               user_move=move.capitalize(),
                                               bot_move=bot_move.capitalize(),
                                               user_score=game['user_score'],
                                               bot_score=game['bot_score'],
                                               ties=game['ties']
                                               )
                                       )

    def _initialize(self, message, best_of):
        self.stats.update({message.author.id: {
            'turn': 1,
            'history': [],
            'user_score': 0,
            'bot_score': 0,
            'ties': 0,
            'best_of': best_of,
        }})

    async def command(self, message):
        """
        HuskieBot will play a game of ROCK, PAPER, Scissors with user

        Parameters
        ----------
        message : discord.Message

        Returns
        -------
        str

        """
        # TODO add -c --cancel -r --restart
        args = message.content.split(' ')[1:]
        if len(args) == 0:
            if self.stats.get(message.author.id, None):
                game = self.stats[message.author.id]
                await message.channel.send(
                    'I already have a game started with you.\n'
                    'We are on turn {} with a best of {}.\n'
                    'The current score is {}-{}-{}'.format(game['turn'],
                                                           game['best_of'],
                                                           game['user_score'],
                                                           game['bot_score'],
                                                           game['ties']))
            else:
                self._initialize(message, 3)
                await message.channel.send('Lets play! Send me a move. (!rps rock, !rps paper, !rps scissors)')
        elif len(args) == 1:
            if self.stats.get(message.author.id, None):
                if args[-1].lower() in self.CHOICES:
                    await self._play(message, args[-1].lower())
                else:
                    await message.channel.send('That is not a valid move')
            else:
                try:
                    self._initialize(message, int(args[-1]))
                    await message.channel.send('Lets play! Send me a move. (!rps rock, !rps paper, !rps scissors)')
                except ValueError:
                    # User may have tried to play a move
                    await message.channel.send('We don\'t have a game going. '
                                               'Start a game by using the !{} command'.format(self.trigger))
        else:
            await message.channel.send('That is not a valid argument')
