from __future__ import annotations

import pprint
from typing import TYPE_CHECKING

from src.my_connector.base import AluConnector

if TYPE_CHECKING:
    from lcu_driver.connection import Connection


async def worker_func(connection: Connection) -> None:
    """Print a dictionary that shows how many skin shards of each price tier
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


connector = AluConnector(worker_func)
connector.start()
