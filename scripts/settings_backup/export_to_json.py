from __future__ import annotations

import json
from pathlib import Path
from typing import TYPE_CHECKING

from src.my_connector import AluConnector

if TYPE_CHECKING:
    from aiohttp import ClientResponse
    from lcu_driver.connection import Connection


async def worker_func(connection: Connection, _summoner: ClientResponse) -> None:
    for item in ["game-settings", "input-settings"]:
        req = await connection.request("get", f"/lol-game-settings/v1/{item}")
        data = await req.json()
        # pprint.pprint(gs_json)

        # ensure .temp folder
        backup_dir = "settings/.backup/"
        Path(backup_dir).mkdir(parents=True, exist_ok=True)
        with open(f"{backup_dir}{item}.json", "w") as f:
            json.dump(data, f, indent=4)
        print(f"{item} req status: {req.status}")


connector = AluConnector(worker_func)
connector.start()
