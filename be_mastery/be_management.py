from __future__ import annotations

from typing import TYPE_CHECKING, Mapping, TypedDict

from lcu_driver import Connector

if TYPE_CHECKING:
    from lcu_driver.connection import Connection

connector = Connector()


async def work_func(connection, summoner):
    summoner_id: int = (await summoner.json())["summonerId"]

    # Champion ID - Mastery Level Mapping
    champid_mlvl_map: Mapping = {}

    req1 = await connection.request("get", f"/lol-collections/v1/inventories/{summoner_id}/champion-mastery")
    for item in await req1.json():
        champid_mlvl_map[item["championId"]] = item["championLevel"]

    # Loot
    req2 = await connection.request("get", "/lol-loot/v1/player-loot")

    for item in await req2.json():
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
                req3 = await connection.request(
                    "post",
                    f"/lol-loot/v1/recipes/CHAMPION_RENTAL_disenchant/craft?repeat={disenchant_shards}",
                    data=[item["lootName"]],
                )


@connector.ready
async def connect(connection: Connection):
    print("LCU API is ready to be used.")
    summoner = await connection.request("get", "/lol-summoner/v1/current-summoner")
    if summoner.status != 200:
        print("Please login into your account to change your icon and restart the script...")
    else:
        await work_func(connection, summoner)


@connector.close
async def disconnect(_: Connection):
    print("The client have been closed!")


connector.start()
