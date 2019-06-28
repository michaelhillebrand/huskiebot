from abc import ABC, abstractmethod


class BaseTask(ABC):

    def __init__(self, client=None) -> None:
        if not hasattr(self, 'id'):
            raise AttributeError('Must provide task id')
        self.client = client
        if not self.client:
            raise AttributeError('Must provide Discord client instance')
        super().__init__()

    async def after_task(self):
        pass

    async def before_task(self):
        pass

    async def run(self):
        await self.before_task()
        await self.task()
        await self.after_task()

    @abstractmethod
    async def task(self):
        pass
