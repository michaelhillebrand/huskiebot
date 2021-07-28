import datetime
import logging
import os
import pickle
import random
import string
from typing import List, Tuple

import discord
from discord.ext import commands

from cogs import BASE_PATH
from cogs.base import BaseCog


class TankTactics(BaseCog):

    # parameters
    minimum_players = 2
    board_width = 3
    board_height = 3
    start_time = datetime.time(hour=9)
    end_time = datetime.time(hour=19)
    action_point_time = datetime.time(hour=12)

    # path to persistent storage
    __PATH = f'{BASE_PATH}/tank_tactics.pkl'

    def __init__(self, bot) -> None:
        channel_id = os.getenv('TANK_TACTICS_CHANNEL')
        self.channel = None
        self.game = {
            'players': {},
            'jury_votes': {},
            'actions': [],
        }
        if channel_id:
            # self.channel = 'test'
            if os.path.exists(self.__PATH):
                with open(self.__PATH, 'rb') as f:
                    self.game.update(pickle.load(f))
        else:
            logging.warning('No Tank Tactics channel ID was provided')
        super().__init__(bot)

    def _filled_positions(self) -> List[str]:
        logging.debug('Getting filled positions')
        return [player_info['position'] for player_id, player_info in self.game['players'].items()]

    def _save(self) -> None:
        """Saves game to disk."""
        logging.debug('Saving Tank Tactics Game')
        with open(self.__PATH, 'wb') as f:
            pickle.dump(self.game, f)

    async def _get_starting_position(self) -> str:
        logging.info('Getting a random starting position')
        unique = False
        position = 'A1'
        retry_count = 0
        while not unique:
            logging.debug(f'Try count: {retry_count + 1}')
            row = random.randint(1, self.board_height)
            col = random.choice(string.ascii_uppercase[:self.board_width])
            position = f'{col}{row}'
            if position not in self._filled_positions():
                logging.debug('Unique position found')
                unique = True
            else:
                logging.debug('Position is already filled')
                retry_count += 1

        return position

    async def _time_check(self) -> bool:
        return self.start_time <= datetime.datetime.now().time() <= self.end_time

    @commands.group(invoke_without_command=True)
    async def tank_tactics(self, ctx: commands.Context, *members):
        """
        Start a new game of Tank Tactics.

        Parameters
        ----------
        ctx : discord.ext.commands.Context
        members : Tuple[discord.Member]

        Returns
        -------
        A game

        """
        # TODO check if this was posted in correct channel
        logging.info('Creating new Tank Tactics game')
        if self.game['players'].keys():
            error_message = 'Unable to create new game - game already in progress'
            logging.error(error_message)
            await ctx.channel.send(error_message)
            return
        players = ctx.message.mentions
        if len(players) == 0:
            error_message = 'Unable to create new game - No players were provided'
            logging.error(error_message)
            await ctx.channel.send(error_message)
            return
        elif len(players) < self.minimum_players:
            error_message = 'Unable to create new game - Not enough players'
            logging.error(error_message)
            await ctx.channel.send(error_message)
            return

        logging.debug('Setting up players')
        for player in players:
            self.game['players'].update({player.id: {
                'hp': 3,
                'ap': 0,
                'range': 2,
                'position': await self._get_starting_position()
            }})

        self._save()

        logging.debug('Tank Tactics game successfully set up')
        await ctx.channel.send("I set up the game for you. Good luck!")

    @tank_tactics.command(name='stats')
    async def display_stats(self, ctx: commands.Context) -> None:
        await ctx.channel.send(self.game)

    @tank_tactics.command(name='ap', hidden=True)
    async def add_ap(self, ctx: commands.Context) -> None:
        self.game['players'][ctx.message.author.id]['ap'] += 1
        await ctx.channel.send('OK')

    @tank_tactics.command(name='fire')
    async def fire_cannon(self, ctx: commands.Context, target_position: str = None) -> None:
        # TODO check if right channel
        if target_position is None:
            logging.error('No position given')
            await ctx.channel.send('You are not able to fire (No position given)')
            return

        target_position = target_position.upper()
        logging.info(f'Firing cannon at position {target_position}')

        player_id = ctx.message.author.id

        logging.debug('Checking if allowed to fire')
        if not await self._time_check():
            logging.error(f'Outside of active hours')
            await ctx.channel.send('Actions are not allowed at this time')
            return

        logging.debug('Checking if player is part of the game')
        if player_id not in self.game['players'].keys():
            logging.error(f'Player {player_id} is not in this game')
            await ctx.channel.send('You are not a part of this game')
            return

        player = self.game['players'][player_id]

        logging.debug('Checking if player is alive')
        if player.get('hp', 0) == 0:
            logging.error(f'Player {player_id} is dead')
            await ctx.channel.send('You are not able to fire (Dead)')
            return

        logging.debug('Checking if player has available action points')
        if player.get('ap', 0) == 0:
            logging.error(f'Player {player_id} has no action points')
            await ctx.channel.send('You are not able to fire (No AP)')
            return

        logging.debug('Getting row and column information')
        try:
            current_position = player['position']
            current_col = current_position[:1]
            current_row = int(current_position[1:])
            target_col = target_position[:1]
            target_row = int(target_position[1:])
        except Exception as e:
            logging.error(e)
            await ctx.channel.send('You are not able to fire (Invalid Position)')
            return

        logging.debug('Checking if position is self')
        if target_position == current_position:
            logging.error(f'Position {target_position} is invalid')
            await ctx.channel.send('You are not able to fire (Own space)')
            return

        logging.debug('Checking if position is empty')
        if target_position not in self._filled_positions():
            logging.error(f'Position {target_position} is empty')
            await ctx.channel.send('You are not able to fire (Space is empty)')
            return

        logging.debug('Getting Target ID')
        target_player = None
        target_player_info = None
        for target_player_id, target_player_info in self.game['players'].items():
            if target_player_info.get('position') == target_position:
                target_player = ctx.bot.get_user(target_player_id)
                target_player_info = target_player_info
                break

        logging.debug('Checking if the position is within the board')
        if target_col not in string.ascii_uppercase[:self.board_width] or \
                target_row not in range(1, self.board_height + 1):
            logging.error(f'Position {target_position} is not on the board')
            await ctx.channel.send('You are not able to fire (Off the board)')
            return

        logging.debug('Checking if target is already dead')
        if target_player_info.get('hp') == 0:
            logging.error(f'Target {target_player.mention} is already dead')
            await ctx.channel.send('You are not able to fire (Target is already dead)')
            return

        logging.debug('Checking if position is within range')
        if ord(target_col) not in range(ord(current_col) - player['range'], ord(current_col) + player['range'] + 2) or \
                target_row not in range(current_row - player['range'], current_row + player['range'] + 1):
            logging.error(f'Position {target_position} is out of range')
            await ctx.channel.send('You are not able to fire (Out of range)')
            return

        logging.debug('Updating points')
        self.game['players'][player_id]['ap'] -= 1
        self.game['players'][target_player.id]['hp'] -= 1

        self._save()

        await ctx.channel.send(f'{ctx.message.author.mention} fired at {target_player.mention}')

        logging.debug('Checking if target is dead')
        if self.game['players'][target_player.id]['hp'] == 0:
            await ctx.channel.send(f'{target_player.mention} is DEAD')

    @tank_tactics.command(name='move')
    async def move_player(self, ctx: commands.Context, next_position: str = None) -> None:
        """
        Moves a player to another position.

        Parameters
        ----------
        ctx : discord.ext.commands.Context
        next_position : str

        Returns
        -------
        str

        """
        # TODO check if right channel
        if next_position is None:
            logging.error('No position given')
            await ctx.channel.send('You are not able to move (No position given)')
            return

        next_position = next_position.upper()
        logging.info(f'Moving player {ctx.message.author.name} to position {next_position}')

        player_id = ctx.message.author.id

        logging.debug('Checking if allowed to fire')
        if not await self._time_check():
            logging.error(f'Outside of active hours')
            await ctx.channel.send('Actions are not allowed at this time')
            return

        logging.debug('Checking if player is part of the game')
        if player_id not in self.game['players'].keys():
            logging.error(f'Player {player_id} is not in this game')
            await ctx.channel.send('You are not a part of this game')
            return

        player = self.game['players'][player_id]

        logging.debug('Checking if player is alive')
        if player.get('hp', 0) == 0:
            logging.error(f'Player {player_id} is dead')
            await ctx.channel.send('You are not able to move (Dead)')
            return

        logging.debug('Checking if player has available action points')
        if player.get('ap', 0) == 0:
            logging.error(f'Player {player_id} has no action points')
            await ctx.channel.send('You are not able to move (No AP)')
            return

        logging.debug('Getting row and column information')
        try:
            current_position = player['position']
            current_col = current_position[:1]
            current_row = int(current_position[1:])
            next_col = next_position[:1]
            next_row = int(next_position[1:])
        except Exception as e:
            logging.error(e)
            await ctx.channel.send('You are not able to move (Invalid Position)')
            return

        logging.debug('Checking is position is already filled')
        if next_position in self._filled_positions():
            logging.error(f'Position {next_position} is already filled')
            await ctx.channel.send('You are not able to move (Space is occupied)')
            return

        logging.debug('Checking if the position is within the board')
        if next_col not in string.ascii_uppercase[:self.board_width] or \
                next_row not in range(1, self.board_height + 1):
            logging.error(f'Position {next_position} is not on the board')
            await ctx.channel.send('You are not able to move (Off the board)')
            return

        logging.debug('Checking if position is within range')
        if ord(next_col) not in range(ord(current_col) - 1, ord(current_col) + 2) or \
                next_row not in range(current_row - 1, current_row + 2):
            logging.error(f'Position {next_position} is out of range')
            await ctx.channel.send('You are not able to move (Out of range)')
            return

        logging.debug(f'Setting position for {player_id}')
        self.game['players'][player_id].update({
            'position': next_position,
            'ap': player['ap'] - 1
        })

        self._save()

        await ctx.channel.send(f'{ctx.message.author.mention} moved from {current_position} to {next_position}')
