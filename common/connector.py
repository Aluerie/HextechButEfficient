from __future__ import annotations

import asyncio
import logging
from typing import TYPE_CHECKING, Any

from lcu_driver import Connector

if TYPE_CHECKING:
    from lcu_driver.connection import Connection

log = logging.getLogger(__name__)


class AluConnector(Connector):
    """Aluerie's Connector - 
    Subclass to lcu_driver's Connector aimed to reduce size of code and spam of the same codeblocks.

    Subclasses of AluConnector are supposed to implement the following functions:
    * coroutine `async def callback(self) -> str:`
    which should do the whole work of the supposed script,
    i.e. `be_mass_disenchant.py` it should do the mass disenchanting.
    """

    if TYPE_CHECKING:
        connection: Connection

    def __init__(self):
        # Probable shit-code ahead warning
        # lcu-driver library has a bug/bad design/oversight where
        # on connector.stop() it doesn't properly close the connection/loop
        # meaning with just `super().__init__()` it won't work on multiple GUI button presses
        # because the infinite loop from the first button connector is left behind waiting for a web sockets to proc
        # so one possible solution to this is to register a new loop on each GUI button press
        # it leaves previous infinitely sleeping event loop untouched though...
        # if anybody knows better - hit me up, I beg you.
        # links:
        # https://github.com/sousa-andre/lcu-driver/issues/18
        # https://github.com/sousa-andre/lcu-driver/pull/34
        # todo: open issue in HextechButEfficient repository
        new_loop = asyncio.new_event_loop()
        super().__init__(loop=new_loop)
        self.result: str = 'No result yet'

        # let's continue.
        self._set_event("ready", self.connect)
        self._set_event("disconnect", self.disconnect)

    async def connect(self, _: Connection):
        log.info("LCU API is connected")

        summoner = await self.get("/lol-summoner/v1/current-summoner")
        if summoner.status != 200:
            # silly check if league is not down
            log.warning("Please login into your account and restart the script...")
        else:
            try:
                self.result = await self.callback()
            except Exception as exc:
                self.result = f'Failed with exception:\n{exc.__class__.__name__}: {str(exc)}'

    async def disconnect(self, _: Connection):
        log.info("Finished task. The LCU API client have been closed!")

    async def callback(self) -> str:
        """This function will be called on @ready event

        It is supposed to be implemented by subclasses and do the script job.
        """
        raise NotImplementedError("You need to implement `async def callback(self):` in AluConnector subclasses.")

    # SHORTCUTS

    async def delete(self, endpoint: str, **kwargs: Any):
        """Shortcut: perform DELETE request against LCU API."""
        log.debug("DELETE %s %s", endpoint, kwargs or "")
        return await self.connection.request("delete", endpoint, **kwargs)

    async def get(self, endpoint: str, **kwargs: Any):
        """Shortcut: perform GET request against LCU API."""
        log.debug("GET %s %s", endpoint, kwargs or "")
        return await self.connection.request("get", endpoint, **kwargs)

    async def patch(self, endpoint: str, **kwargs: Any):
        """Shortcut: perform PATCH request against LCU API."""
        log.debug("PATCH %s %s", endpoint, kwargs or "")
        return await self.connection.request("patch", endpoint, **kwargs)

    async def post(self, endpoint: str, **kwargs: Any):
        """Shortcut: perform POST request against LCU API."""
        log.debug("POST %s %s", endpoint, kwargs or "")
        return await self.connection.request("post", endpoint, **kwargs)

    async def put(self, endpoint: str, **kwargs: Any):
        """Shortcut: perform PUT request against LCU API."""
        log.debug("PUT %s %s", endpoint, kwargs or "")
        return await self.connection.request("put", endpoint, **kwargs)
