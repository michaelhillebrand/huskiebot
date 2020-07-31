import datetime
import math
import random

from discord.ext import commands, tasks

from cogs.base import BaseCog


class RockPaperScissors(BaseCog):
    stats = {}

    ROCK = 'rock'
    PAPER = 'paper'
    SCISSORS = 'scissors'

    CHOICES = [ROCK, PAPER, SCISSORS]

    # bot move is first, human move is second. result is for human
    MATRIX = {
        ROCK: {
            PAPER: 1,
            SCISSORS: -1
        },
        PAPER: {
            SCISSORS: 1,
            ROCK: -1
        },
        SCISSORS: {
            ROCK: 1,
            PAPER: -1
        }
    }

    def _initialize(self, ctx, best_of):
        self.stats.update({ctx.author.id: {
            'turn': 1,
            'history': [],
            'user_score': 0,
            'bot_score': 0,
            'ties': 0,
            'best_of': best_of,
            'last_played': datetime.datetime.utcnow()
        }})

    @tasks.loop(hours=1)
    async def game_cleaner(self):
        """Cleans old games to save RAM."""
        to_remove = [player_id for player_id, game in self.stats.items()
                     if (game['last_played'] + datetime.timedelta(hours=1)) < datetime.datetime.utcnow()]
        for player_id in to_remove:
            del self.stats[player_id]

    @commands.group(invoke_without_command=True)
    async def rps(self, ctx: commands.Context, move: str = ''):
        """
        HuskieBot will play a game of Rock, Paper, Scissors with user

        Parameters
        ----------
        ctx : discord.ext.commands.Context
        move : str

        Returns
        -------
        str

        """
        human_move = move.lower()
        game = self.stats.get(ctx.author.id)
        if game:
            bot_move = random.choice(self.CHOICES)
            try:
                result = 0 if human_move == bot_move else self.MATRIX[bot_move][human_move]
            except KeyError:
                await ctx.send("That is not a valid move")
                return
            if result == 1:
                field = 'user_score'
            elif result == -1:
                field = 'bot_score'
            else:
                field = 'ties'
            game.update({
                'turn': game['turn'] + 1,
                'history': game['history'].append({'bot': bot_move, 'user': human_move, 'result': result}),
                'last_played': datetime.datetime.utcnow(),
                field: game[field] + 1
            })
            if max(game['user_score'], game['bot_score']) >= math.ceil(game['best_of'] / 2):
                await ctx.send(f'{ctx.author.mention}\t\t\tHuskieBot\n'
                               f'{human_move.capitalize()}\tvs.\t{bot_move.capitalize()}\n'
                               f'GAME OVER\n'
                               f'Final Score: {game["user_score"]}-{game["bot_score"]}-{game["ties"]}\n\n'
                               f'Want to play again?')
                self.stats.pop(ctx.author.id, None)
            else:
                await ctx.send(f'{ctx.author.mention}\t\t\tHuskieBot\n'
                               f'{human_move.capitalize()}\tvs.\t{bot_move.capitalize()}\n'
                               f'Current Score: {game["user_score"]}-{game["bot_score"]}-{game["ties"]}')
        else:
            await ctx.send(f'We don\'t have a game going. Start a game by using the "!{ctx.command} start" command')

    @rps.command(name='stop')
    async def rps_stop(self, ctx: commands.Context):
        """
        HuskieBot will clear the game it is currently playing with the user.

        Parameters
        ----------
        ctx : discord.ext.commands.Context

        Returns
        -------
        Int
            The number of dank images in the media folder

        """
        game = self.stats.get(ctx.author.id)
        if game:
            self.stats.pop(ctx.author.id, None)
            await ctx.send(f"Thanks for rage quitting! Try not to be so salty next time")
        else:
            await ctx.send(f"I don't have a game started with you")

    @rps.command(name='start')
    async def rps_start(self, ctx: commands.Context):
        """
        HuskieBot will start a new game with the user.

        Parameters
        ----------
        ctx : discord.ext.commands.Context

        Returns
        -------
        Int
            The number of dank images in the media folder

        """
        game = self.stats.get(ctx.author.id)
        if game:
            await ctx.send(
                f"I already have a game started with you.\n"
                f"We are on turn {game['turn']} with a best of {game['best_of']}.\n"
                f"The current score is {game['user_score']}-{game['bot_score']}-{game['ties']}")
        else:
            self._initialize(ctx, 3)
            await ctx.send('Lets play! Send me a move (!rps rock, !rps paper, !rps scissors)')
