from __future__ import annotations

import asyncio
import logging
from typing import TYPE_CHECKING, Any

from lcu_driver import Connector

from gui.confirmation import ConfirmationBox

from .errors import ConfirmationDenied, CustomException

if TYPE_CHECKING:
    from lcu_driver.connection import Connection

    from .schemas import *

log = logging.getLogger(__name__)

# I'm doing it here so all if __main__ == '__main__': also get logging
logging.basicConfig(
    format="{asctime} | {levelname:<7} | {funcName:<30} | {message}",
    datefmt="%H:%M:%S %d/%m",
    style="{",
    level=logging.INFO,
)


class AluConnector(Connector):
    """Aluerie's Connector -
    Subclass to lcu_driver's Connector aimed to reduce size of code and spam of the same codeblocks.

    Subclasses of AluConnector are supposed to implement the following functions:
    * coroutine `async def callback(self) -> str:`
    which should do the whole work of the supposed script,
    i.e. `be_mass_disenchant.py` it should do the mass disenchanting.

    Also doc-strings of AluConnector subclasses should be written
    in user-friendly way since they are going to be shown to them.
    """

    if TYPE_CHECKING:
        connection: Connection
        summoner_id: int  # used in many requests so let's keep it close

    def __init__(self, need_confirmation: bool = False):
        new_loop = asyncio.new_event_loop()
        super().__init__(loop=new_loop)
        self.console_text: str = "No result yet"
        self.need_confirmation: bool = need_confirmation

        self._set_event("ready", self.connect)
        self._set_event("disconnect", self.disconnect)

    async def connect(self, _: Connection):
        log.info("LCU API is connected")

        r_summoner = await self.get("/lol-summoner/v1/current-summoner")
        if r_summoner.status != 200:
            # silly check if league is not down
            log.warning("Please login into your account and restart the script...")
        else:
            try:
                self.summoner_id: int = (await r_summoner.json())["summonerId"]
                self.console_text = await self.callback()
                log.info(self.console_text)
            except Exception as exc:
                if isinstance(exc, CustomException):
                    self.console_text = str(exc)
                    log.info(exc)
                else:
                    self.console_text = (
                        f"Failed with exception. Contact developers about it:" f"\n{exc.__class__.__name__}: {str(exc)}"
                    )
                    log.error("%s: %s", exc.__class__.__name__, exc, exc_info=True)

    async def disconnect(self, _: Connection):
        log.info("Finished task. The LCU API client have been closed!")

    async def callback(self) -> str:
        """This function will be called on @ready event

        It is supposed to be implemented by subclasses and do the script job.

        * For streamlined UI experience callbacks should at some point
            call self.confirm or self.output to showcase their results.

        * And it also should return a small descriptive string to print in the GUI console.
        """
        raise NotImplementedError("You need to implement `async def callback(self):` in AluConnector subclasses.")

    def confirm(self, script_message: str) -> bool:
        """Bring Confirmation dialog that describes what the script gonna do

        This function is made to used in callback body to request confirming loot-sensitive scripts like disenchant.
        It can be defaulted to skip confirmation if self.need_confirmation is False
        """
        log.info(script_message)
        if not self.need_confirmation:
            # no confirmation is needed
            return True

        confirm = ConfirmationBox(script_message).get()
        if not confirm:
            # user pressed No, closed the window or etc.
            raise ConfirmationDenied("Confirmation was not received. Not executing.")
        else:
            # user pressed Yes
            return True

    def output(self, script_message: str):
        """Bring OK-confirmation dialog that shows the script output to user.

        If the script is not loot-sensitive then we can just show the result of the script.
        """
        log.info(script_message)
        if not self.need_confirmation:
            # no confirmation is needed
            return

        ConfirmationBox(script_message, option_no=False)

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

    # LCU API WRAPPER LIKE TYPING FRIENDLY REQUESTS

    async def get_lol_champions_v1_inventories_skins_minimal(self) -> list[MinimalSkin]:
        """Get skins minimal."""
        r_skins = await self.get(f"/lol-champions/v1/inventories/{self.summoner_id}/skins-minimal")
        return await r_skins.json()

    async def get_lol_loot_v1_player_loot(self) -> list[LootItem]:
        """Get player loot."""
        r_loot = await self.get("/lol-loot/v1/player-loot")
        return await r_loot.json()

    async def get_lol_collections_v1_inventories_champion_mastery(self) -> list[ChampionMastery]:
        """Get champion mastery."""
        r_mastery = await self.get(f"/lol-collections/v1/inventories/{self.summoner_id}/champion-mastery")
        return await r_mastery.json()