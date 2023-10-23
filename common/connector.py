from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING, Protocol

from lcu_driver import Connector

if TYPE_CHECKING:
    from lcu_driver.connection import Connection


class WorkerFunc(Protocol):
    async def __call__(self, connection: Connection) -> None:
        ...


class AluConnector(Connector):
    """My subclass to lcu_driver's Connector

    Just to reduce spam of the same code block.

    How to use this:

    >>> from src.my_connector import AluConnector
    >>> # later
    >>> connector = AluConnector(worker_func)
    >>> connector.start()

    Note that worker_func is supposed to be of the WorkerFunction signature shown above^:
    worker_func is supposed to do the job in a script.
    """

    def __init__(self, coro_func: WorkerFunc):
        new_loop = asyncio.new_event_loop()  # idk asyncio stuff well but it errors out otherwise
        super().__init__(loop=new_loop)
        self.coro_func: WorkerFunc = coro_func
        self._set_event("ready", self.connect)
        self._set_event("disconnect", self.disconnect)

    async def connect(self, connection: Connection):
        print("LCU API is ready to be used.")
        summoner = await connection.request("get", "/lol-summoner/v1/current-summoner")
        if summoner.status != 200:  # this is actually pointless since there s no login screen anymore
            print("Please login into your account and restart the script...")
        else:
            await self.coro_func(connection)

    async def disconnect(self, _: Connection):
        print("Finished task. The LCU API client have been closed!")
