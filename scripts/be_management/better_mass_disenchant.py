from __future__ import annotations

from typing import TYPE_CHECKING, Mapping

from src.my_connector import AluConnector

if TYPE_CHECKING:
    from aiohttp import ClientResponse
    from lcu_driver.connection import Connection


async def worker_func(connection: Connection, summoner: ClientResponse) -> None:
    summoner_id: int = (await summoner.json())["summonerId"]

    # Champion ID - Mastery Level Mapping
    champid_mlvl_map: Mapping = {}

    mastery_req = await connection.request("get", f"/lol-collections/v1/inventories/{summoner_id}/champion-mastery")
    for item in await mastery_req.json():
        champid_mlvl_map[item["championId"]] = item["championLevel"]

    # Loot
    loot_req = await connection.request("get", "/lol-loot/v1/player-loot")

    for item in await loot_req.json():
        if item["type"] == "CHAMPION_RENTAL":
            if item["itemStatus"] == "OWNED":
                champ_id = item["storeItemId"]
                if champ_id in champid_mlvl_map:
                    if champid_mlvl_map[champ_id] == 7:
                        save_shards = 0
                    elif champid_mlvl_map[champ_id] == 6:
                        save_shards = 1
                    else:
                        save_shards = 2
                else:
                    save_shards = 2
            else:
                save_shards = 3

            disenchant_shards = max(0, item["count"] - save_shards)

            if disenchant_shards:
                disenchant_req = await connection.request(
                    "post",
                    f"/lol-loot/v1/recipes/CHAMPION_RENTAL_disenchant/craft?repeat={disenchant_shards}",
                    data=[item["lootName"]],
                )


connector = AluConnector(worker_func)
connector.start()
