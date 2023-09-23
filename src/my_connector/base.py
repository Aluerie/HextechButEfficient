from __future__ import annotations

from typing import TYPE_CHECKING

from lcu_driver import Connector

if TYPE_CHECKING:
    from lcu_driver.connection import Connection


class AluConnector(Connector):
    def __init__(
        self,
        coro_func,
        *,
        loop=None,
    ):
        super().__init__(loop=loop)

        self.coro_func = coro_func
        self._set_event("ready", self.connect)
        self._set_event("disconnect", self.disconnect)

    async def connect(self, connection: Connection):
        print("LCU API is ready to be used.")
        summoner = await connection.request("get", "/lol-summoner/v1/current-summoner")
        if summoner.status != 200:
            print("Please login into your account and restart the script...")
        else:
            await self.coro_func(connection)

    async def disconnect(self, _: Connection):
        print("The LCU API client have been closed!")
