import datetime
import logging
import os
import pickle
import random
import string
from tempfile import NamedTemporaryFile
from typing import List, Tuple

import discord
from PIL import Image, ImageDraw
from discord.ext import commands

from cogs import BASE_PATH
from cogs.base import BaseCog


# TODO optimize requirements check
class TankTactics(BaseCog):

    # parameters
    minimum_players = 2
    board_width = 18
    board_height = 13
    start_time = datetime.time(hour=9)
    end_time = datetime.time(hour=21)
    action_point_time = datetime.time(hour=12)  # Time of day

    # path to persistent storage
    __PATH = f'{BASE_PATH}/tank_tactics.pkl'

    HEALTH = 'hp'
    RANGE = 'range'
    UPGRADE_CHOICES = [
        HEALTH,
        RANGE
    ]
    ACTION = 'ap'
    GIVE_CHOICES = [
        HEALTH,
        ACTION
    ]

    def __init__(self, bot) -> None:
        self.channel_id = os.getenv('TANK_TACTICS_CHANNEL')
        self.map_channel_id = os.getenv('TANK_TACTICS_MAP_CHANNEL')
        self.game = {
            'players': {},
            'jury_votes': {},
            'actions': [],
            'heart_position': None
        }
        if self.channel_id:
            if os.path.exists(self.__PATH):
                with open(self.__PATH, 'rb') as f:
                    self.game.update(pickle.load(f))
        else:
            logging.warning('No Tank Tactics channel ID was provided')
        super().__init__(bot)

    async def _filled_player_positions(self) -> List[str]:
        """
        Returns a list of filled positions by players on the board.

        Returns
        -------
        An Array of positions filled by other players

        """
        logging.debug('Getting filled positions')
        return [player_info['position'] for player_id, player_info in self.game['players'].items()]

    async def _filled_positions(self) -> List[str]:
        """
        Returns a list of filled positions on the board.

        Returns
        -------
        An Array of positions filled by other objects

        """
        logging.debug('Getting filled positions')
        filled_positions = await self._filled_player_positions()
        if self.game['heart_position']:
            filled_positions.append(self.game['heart_position'])
        return filled_positions

    async def _save(self) -> None:
        """Saves game to disk."""
        logging.debug('Saving Tank Tactics Game')
        with open(self.__PATH, 'wb') as f:
            pickle.dump(self.game, f)

    async def _get_random_position(self) -> str:
        """
        Returns a blank random position from the board

        Returns
        -------
        A position from the board

        """
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

    async def _get_alive_players(self) -> dict:
        return {k: v for k, v in self.game['players'].items() if v['hp'] > 0}

    async def draw_map(self) -> None:
        channel = self.bot.get_channel(int(self.map_channel_id))
        if not channel:
            logging.error('Channel ID was invalid')
            raise ValueError

        offset = 100

        image = Image.new(mode='RGB', size=(
            (self.board_width + 1) * offset,
            (self.board_height + 1) * offset
        ), color='white')
        draw = ImageDraw.Draw(image)
        step_size = offset

        logging.debug('Drawing vertical lines')
        y_start = 0
        y_end = image.height
        for x, letter in zip(range(0, image.width, step_size), string.ascii_uppercase):
            line = ((x, y_start), (x, y_end))
            draw.line(line, width=5 if x == offset else 1, fill='black')
            if x != self.board_width:
                draw.text((x + offset + 5, y_start + 5), letter, fill='black')

        logging.debug('Drawing horizontal lines')
        x_start = 0
        x_end = image.width
        for y, row_number in zip(range(0, image.height, step_size), range(1, self.board_height + 2)):
            line = ((x_start, y), (x_end, y))
            draw.line(line, width=5 if y == offset else 1, fill='black')
            if y != self.board_height:
                draw.text((x_start + 5, y + offset + 5), str(row_number), fill='black')

        logging.debug('Drawing players')
        for player_id, player_info in self.game['players'].items():
            player = await self.bot.fetch_user(player_id)
            x = (ord(player_info['position'][:1]) - 65) * 100 + offset
            y = (int(player_info['position'][1:]) - 1) * 100 + offset
            fill_color = 'black' if player_info['hp'] == 0 else 'blue'
            draw.rectangle((x, y, x + 100, y + 100), fill=fill_color)
            draw.text(
                (x + 5, y + 5),
                f"{player.name}\n"
                f"HP: {player_info['hp']}\n"
                f"AP: {player_info['ap']}\n"
                f"Range: {player_info['range']}"
            )

        if self.game.get('heart_position'):
            logging.debug('Drawing heart')
            x = (ord(self.game['heart_position'][:1]) - 65) * 100 + offset
            y = (int(self.game['heart_position'][1:]) - 1) * 100 + offset
            draw.rectangle((x, y, x + 100, y + 100), fill='red')
            draw.text((x + 5, y + 5), "HEART", fill='white')

        del draw

        with NamedTemporaryFile() as tmp_file:
            image.save(tmp_file.name, format='JPEG')
            await channel.send(file=discord.File(tmp_file.name, f'tank_tactics_map_{datetime.datetime.now()}.jpg'))

        # image.show()

    async def place_heart(self) -> None:
        logging.info('Placing Heart on map')
        if self.game.get('heart_position'):
            logging.info('Heart is already on the map')
        else:
            self.game.update({'heart_position': await self._get_random_position()})

    async def kill_player(self, ctx, player) -> None:
        self.game['players'][player.id].update({
            'hp': 0,
            'ap': 0
        })
        await self._save()
        await ctx.channel.send(f'{player.mention} is DEAD')

    async def start_counsel(self) -> None:
        logging.info('Starting Counsel')

        logging.debug('Checking if enough people in jury')
        if len(self.game['jury_votes']) < 3:
            logging.info('Not enough people in jury to make a ruling')
            self.game.update({'jury_votes': {}})
            await self._save()
            return

        logging.debug('Gathering votes')
        votes = sorted(self.game['jury_votes'].items(), key=lambda x: x[-1])

        logging.debug('Giving Action Point to majority vote')
        self.game['players'][votes[0][0]]['ap'] += 1

        del votes
        self.game.update({'jury_votes': {}})

        await self._save()

    async def start_day(self):
        await self.bot.wait_until_ready()
        channel = self.bot.get_channel(int(self.channel_id))
        if not channel:
            logging.error('Channel ID was invalid')
            raise ValueError

        logging.info('Starting new day')

        logging.debug('Giving out Action Points')
        alive_players = await self._get_alive_players()
        for player_id, _ in alive_players.items():
            self.game['players'][player_id]['ap'] += 1

        await self.place_heart()

        await self.start_counsel()

        await self.draw_map()

        await channel.send('A new day has started')

    @commands.group(name='tt', invoke_without_command=True)
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
                'position': await self._get_random_position()
            }})

        await self.place_heart()

        await self._save()

        logging.debug('Tank Tactics game successfully set up')
        await ctx.channel.send("I set up the game for you. Good luck!")

        await self.draw_map()

    @tank_tactics.command(name='fire')
    async def fire_cannon(self, ctx: commands.Context) -> None:
        # TODO check if right channel
        logging.debug('Checking if correct number of players was provided')
        if len(ctx.message.mentions) == 0:
            logging.error('No player given')
            await ctx.channel.send('You are not able to fire (No players provided)')
            return
        elif len(ctx.message.mentions) > 1:
            logging.error('Too many players provided')
            await ctx.channel.send('You are not able to fire (Only 1 player at a time)')
            return

        target_player = ctx.message.mentions[0]
        logging.info(f'Firing cannon at player {target_player.id}')

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

        player_info = self.game['players'][player_id]
        target_player_info = self.game['players'][target_player.id]

        logging.debug('Checking if player is alive')
        if player_info.get('hp', 0) == 0:
            logging.error(f'Player {player_id} is dead')
            await ctx.channel.send('You are not able to fire (Dead)')
            return

        logging.debug('Checking if player has available action points')
        if player_info.get('ap', 0) == 0:
            logging.error(f'Player {player_id} has no action points')
            await ctx.channel.send('You are not able to fire (No AP)')
            return

        logging.debug('Getting row and column information')
        try:
            target_position = target_player_info['position']
            current_col = player_info['position'][:1]
            current_row = int(player_info['position'][1:])
            target_col = target_player_info['position'][:1]
            target_row = int(target_player_info['position'][1:])
        except Exception as e:
            logging.error(e)
            await ctx.channel.send('You are not able to fire (Invalid Position)')
            return

        logging.debug('Checking if player is self')
        if target_player.id == ctx.message.author.id:
            logging.error(f'Position {target_position} is invalid')
            await ctx.channel.send('You are not able to fire (yourself)')
            return

        logging.debug('Checking if target is already dead')
        if target_player_info.get('hp') == 0:
            logging.error(f'Target {target_player.id} is already dead')
            await ctx.channel.send('You are not able to fire (Target is already dead)')
            return

        logging.debug('Checking if position is within range')
        if ord(target_col) not in range(ord(current_col) - player_info['range'], ord(current_col) + player_info['range'] + 2) or \
                target_row not in range(current_row - player_info['range'], current_row + player_info['range'] + 1):
            logging.error(f'Position {target_position} is out of range')
            await ctx.channel.send('You are not able to fire (Out of range)')
            return

        logging.debug('Updating points')
        self.game['players'][player_id]['ap'] -= 1
        self.game['players'][target_player.id]['hp'] -= 1

        await self._save()

        await self.draw_map()

        await ctx.channel.send(f'{ctx.message.author.mention} fired at {target_player.mention}')

        logging.debug('Checking if target is dead')
        if self.game['players'][target_player.id]['hp'] == 0:
            await self.kill_player(ctx, target_player)

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

        logging.debug('Checking if allowed to move')
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
        if next_position in self._filled_player_positions():
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

        healed = False
        logging.debug('Checking if heart is in position')
        if next_position == self.game.get('heart_position', ''):
            healed = True
            del self.game['heart_position']

        logging.debug(f'Setting position for {player_id}')
        self.game['players'][player_id].update({
            'position': next_position,
            'ap': player['ap'] - 1,
            'hp': (player['hp'] + 1) if healed else player['hp']
        })

        await self._save()

        await self.draw_map()

        await ctx.channel.send(f'{ctx.message.author.mention} moved from {current_position} to {next_position}')

    @tank_tactics.command(name='give')
    async def give(self, ctx: commands.Context, choice: str) -> None:
        # TODO check if right channel
        logging.debug('Checking if correct number of players was provided')
        if len(ctx.message.mentions) == 0:
            logging.error('No player given')
            await ctx.channel.send('You are not able to trade (No players provided)')
            return
        elif len(ctx.message.mentions) > 1:
            logging.error('Too many players provided')
            await ctx.channel.send('You are not able to trade (Only 1 player at a time)')
            return
        elif choice not in self.GIVE_CHOICES:
            logging.error('Invalid Give choice provided')
            await ctx.channel.send('You are not able to trade (Only 1 player at a time)')
            return

        target_player = ctx.message.mentions[0]

        player_id = ctx.message.author.id

        logging.debug('Checking if allowed to give')
        if not await self._time_check():
            logging.error(f'Outside of active hours')
            await ctx.channel.send('Actions are not allowed at this time')
            return

        logging.debug('Checking if player is part of the game')
        if player_id not in self.game['players'].keys():
            logging.error(f'Player {player_id} is not in this game')
            await ctx.channel.send('You are not a part of this game')
            return

        player_info = self.game['players'][player_id]
        target_player_info = self.game['players'][target_player.id]

        logging.debug('Checking if player is alive')
        if player_info.get('hp', 0) == 0:
            logging.error(f'Player {player_id} is dead')
            await ctx.channel.send('You are not able to trade (Dead)')
            return

        logging.debug('Getting row and column information')
        try:
            current_col = player_info['position'][:1]
            current_row = int(player_info['position'][1:])
            target_col = target_player_info['position'][:1]
            target_row = int(target_player_info['position'][1:])
        except Exception as e:
            logging.error(e)
            await ctx.channel.send('You are not able to trade (Invalid Position)')
            return

        logging.debug('Checking if position is within range')
        if ord(target_col) not in range(ord(current_col) - player_info['range'], ord(current_col) + player_info['range'] + 2) or \
                target_row not in range(current_row - player_info['range'], current_row + player_info['range'] + 1):
            logging.error(f'Player {target_player.id} is out of range')
            await ctx.channel.send('You are not able to trade (Out of range)')
            return

        if choice == self.ACTION:
            logging.debug('Checking if player has available action points')
            if player_info.get('ap', 0) == 0:
                logging.error(f'Player {player_id} has no action points')
                await ctx.channel.send('You are not able to trade (No AP)')
                return
            logging.debug('Adjusting Action Points')
            self.game['players'][player_id]['ap'] -= 1
            self.game['players'][target_player.id]['ap'] += 1

        elif choice == self.HEALTH:
            logging.debug('Checking if player has available Health Points')
            if player_info.get('hp', 0) <= 1:
                logging.error(f'Player {player_id} has no Health Points to give')
                await ctx.channel.send('You are not able to trade (No available HP)')
                return
            logging.debug('Adjusting Health Points')
            self.game['players'][player_id]['hp'] -= 1
            self.game['players'][target_player.id]['hp'] += 1

        await self._save()

        await self.draw_map()

        await ctx.channel.send(f'{ctx.message.author.mention} gave {target_player.mention} '
                               f'{"an Action Point" if choice == self.ACTION else "a Health Point"}')

    @tank_tactics.command(name='upgrade')
    async def upgrade(self, ctx: commands.Context, option: str = None) -> None:
        # TODO check if right channel
        if option is None:
            logging.error('No option given')
            await ctx.channel.send('You are not able to upgrade (No option given)')
            return
        elif option not in self.UPGRADE_CHOICES:
            logging.error('Invalid option given')
            await ctx.channel.send('You are not able to upgrade (Invalid option given)')
            return

        logging.info(f'Player {ctx.message.author.id} is upgrading')

        player_id = ctx.message.author.id

        logging.debug('Checking if allowed to upgrade')
        if not await self._time_check():
            logging.error(f'Outside of active hours')
            await ctx.channel.send('Actions are not allowed at this time')
            return

        logging.debug('Checking if player is part of the game')
        if player_id not in self.game['players'].keys():
            logging.error(f'Player {player_id} is not in this game')
            await ctx.channel.send('You are not a part of this game')
            return

        player_info = self.game['players'][player_id]

        logging.debug('Checking if player has available Action Points')
        if player_info.get('ap', 0) < 3:
            logging.error(f'Player {player_id} does not have enough Action Points')
            await ctx.channel.send('You are not able to upgrade (Not enough AP)')
            return

        logging.debug('Adjusting range')
        self.game['players'][player_id].update({
            option: player_info[option] + 1,
            'ap': player_info['ap'] - 3
        })

        await self._save()

        await self.draw_map()

        await ctx.channel.send(f'{ctx.message.author.mention} has upgraded their {option}')

    @tank_tactics.command(name='vote')
    async def jury_vote(self, ctx: commands.Context) -> None:
        # TODO check if right channel
        logging.debug('Checking if correct number of players was provided')
        if len(ctx.message.mentions) == 0:
            logging.error('No player given')
            await ctx.channel.send('You are not able to vote (No players provided)')
            return
        elif len(ctx.message.mentions) > 1:
            logging.error('Too many players provided')
            await ctx.channel.send('You are not able to vote (Only 1 player at a time)')
            return

        target_player = ctx.message.mentions[0]

        logging.info(f'Player {ctx.message.author.id} is voting for player {target_player.id}')

        player_id = ctx.message.author.id

        logging.debug('Checking if allowed to vote')
        if not await self._time_check():
            logging.error(f'Outside of active hours')
            await ctx.channel.send('Actions are not allowed at this time')
            return

        logging.debug('Checking if player is part of the game')
        if player_id not in self.game['players'].keys():
            logging.error(f'Player {player_id} is not in this game')
            await ctx.channel.send('You are not a part of this game')
            return

        logging.debug('Checking if player is part of the game')
        if self.game['jury_votes'].get(ctx.message.author.id, False):
            logging.error(f'Player {player_id} has already voted today')
            await ctx.channel.send('YYou are not able to vote (Already voted)')
            return

        player_info = self.game['players'][player_id]

        logging.debug('Checking if player is dead')
        if player_info.get('hp', 0) > 0:
            logging.error(f'Player {player_id} is alive')
            await ctx.channel.send('You are not able to vote (Alive)')
            return

        logging.debug('Adding Vote')
        vote_count = self.game['jury_votes'].get(target_player.id, 0)
        self.game['jury_votes'][target_player.id] = vote_count + 1

        await self._save()

        await ctx.channel.send(f'{ctx.message.author.mention} voted for {target_player.mention}')
