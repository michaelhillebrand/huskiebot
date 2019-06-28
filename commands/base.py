from abc import ABC, abstractmethod


class BaseCommand(ABC):

    def __init__(self, client=None) -> None:
        if not hasattr(self, 'trigger'):
            raise AttributeError('Must provide trigger')
        if not hasattr(self, 'description'):
            raise AttributeError('Must provide description for commands list')
        if not client:
            raise AttributeError('Must provide Discord client instance')
        self.client = client
        super().__init__()

    async def on_ready(self):
        pass

    async def after_command(self, message):
        pass

    async def before_command(self, message):
        pass

    async def run(self, message):
        await self.before_command(message)
        await self.command(message)
        await self.after_command(message)

    @abstractmethod
    async def command(self, message):
        pass
