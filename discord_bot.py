import os

import discord

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
MEDIA_PATH = os.path.join(BASE_PATH, 'media/')
if not os.path.exists(MEDIA_PATH):
    os.makedirs(MEDIA_PATH)


class HuskieBot(discord.Client):

    def __init__(self, *, loop=None, commands=None, tasks=None, **options):
        if tasks is None:
            tasks = []
        if commands is None:
            commands = []
        self.tasks = {task.id: task(self) for task in tasks}
        self.commands = {command.trigger: command(self) for command in commands}
        super().__init__(loop=loop, **options)

    async def add_commands(self, commands):
        """
        Adds commands to HuskieBot's list
        :param commands:
        :return None:
        """
        self.commands.update({command.trigger: command(self) for command in commands})

    async def add_tasks(self, tasks):
        """
        Adds tasks to HuskieBot's list
        :param tasks:
        :return None:
        """
        initialized_tasks = {task.id: task(self) for task in tasks}
        self.tasks.update(initialized_tasks)
        [self.loop.create_task(task.run()) for task_id, task in initialized_tasks.items()]

    async def on_ready(self):
        """
        HuskieBot is ready to accept messages

        Runs on_ready callback for commands
        Runs tasks
        :return None:
        """
        [self.loop.create_task(command.on_ready()) for _, command in self.commands.items()]
        [self.loop.create_task(task.run()) for _, task in self.tasks.items()]
        print('Huskie Bot Online')

    async def on_message(self, message):
        """
        Receives and processes message
        :param message:
        :return None:
        """
        # we do not want the bot to reply to itself
        if message.author == self.user:
            return

        elif message.content.startswith('!commands'):
            await message.channel.send('```{}```'.format('\n'.join(['!{trigger}{spacing}- {description}'.format(
                trigger=command.trigger,
                spacing=' ' * (max([len(trigger) for trigger in self.commands.keys()]) + 4 - len(command.trigger)),
                description=command.description
            ) for _, command in sorted(self.commands.items())])))

        elif message.content[0] == '!':
            trigger = message.content.split(' ')[0][1:]
            try:
                await self.commands[trigger].run(message)
            except KeyError:
                await message.channel.send('That is not a valid command')
