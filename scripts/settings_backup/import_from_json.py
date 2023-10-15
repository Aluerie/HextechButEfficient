from __future__ import annotations

import json
from typing import TYPE_CHECKING

from src.my_connector import AluConnector

if TYPE_CHECKING:
    from aiohttp import ClientResponse
    from lcu_driver.connection import Connection


async def worker_func(connection: Connection, summoner: ClientResponse) -> None:
    for item in ["game-settings", "input-settings"]:
        f = open(f"scripts/settings_backup/.backup/{item}.json")
        data = json.load(f)
        req = await connection.request("patch", f"/lol-game-settings/v1/{item}", data=data)
        print(f"{item} req status: {req.status}")


connector = AluConnector(worker_func)
connector.start()
