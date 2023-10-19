from __future__ import annotations

from typing import TYPE_CHECKING, Protocol

from lcu_driver import Connector

if TYPE_CHECKING:
    from aiohttp import ClientResponse
    from lcu_driver.connection import Connection


class WorkerFunc(Protocol):
    async def __call__(self, connection: Connection, summoner: ClientResponse) -> None:
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

    def __init__(self, coro_func: WorkerFunc, *, loop=None):
        super().__init__(loop=loop)
        self.coro_func: WorkerFunc = coro_func
        self._set_event("ready", self.connect)
        self._set_event("disconnect", self.disconnect)

    async def connect(self, connection: Connection):
        print("LCU API is ready to be used.")
        summoner = await connection.request("get", "/lol-summoner/v1/current-summoner")
        if summoner.status != 200:
            print("Please login into your account and restart the script...")
        else:
            await self.coro_func(connection, summoner)

    async def disconnect(self, _: Connection):
        print("The LCU API client have been closed!")
