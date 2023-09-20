from __future__ import annotations

import pprint
from typing import TYPE_CHECKING

from lcu_driver import Connector

if TYPE_CHECKING:
    from lcu_driver.connection import Connection

connector = Connector()


async def worker_func(connection: Connection) -> None:
    """Main function of this script.

    Which is to print a dictionary that shows how many skin shards of each price tier
    I own/do not own.

    This information gets pasted into excel spreadsheet for further and more visually appealing math.

    Example output:
    >>> {520: {'not_owned': 3, 'owned': 0}, ... 1820: {'not_owned': 67, 'owned': 19}}
    """

    req = await connection.request("get", f"/lol-loot/v1/player-loot")
    player_loot_json = await req.json()

    skin_shards = [item for item in player_loot_json if item["displayCategories"] == "SKIN"]

    shard_categories = {k: {"owned": 0, "not_owned": 0} for k in [520, 750, 975, 1350, 1820]}

    for shard in skin_shards:
        if shard["itemStatus"] == "OWNED":
            shard_categories[shard["value"]]["owned"] += shard["count"]
        else:
            shard_categories[shard["value"]]["not_owned"] += 1
            shard_categories[shard["value"]]["owned"] += shard["count"] - 1

    pprint.pprint(shard_categories)


@connector.ready
async def connect(connection: Connection):
    print("LCU API is ready to be used.")
    summoner = await connection.request("get", "/lol-summoner/v1/current-summoner")
    if summoner.status != 200:
        print("Apparently, you are not logged in. Please, login into your account and restart the script...")
    else:
        await worker_func(connection)


@connector.close
async def disconnect(_: Connection):
    print("The LCU API client have been closed!")


connector.start()
