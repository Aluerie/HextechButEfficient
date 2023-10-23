"""
# Mass-Disenchant Champion Shards accounting for Mastery levels.

- [X] keep 3/2/1/0 champion shards depending on their mastery - 
respectively to not_owned/5_and_below/6/7 level.
- [ ] Disenchant permanent shards for owned champions.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Mapping

from common.connector import AluConnector

if TYPE_CHECKING:
    from lcu_driver.connection import Connection


async def worker_func(connection: Connection) -> None:
    summoner = await connection.request("get", "/lol-summoner/v1/current-summoner")
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
                        save_shards = 0  # mastery 7 champ
                    elif champid_mlvl_map[champ_id] == 6:
                        save_shards = 1  # mastery 6 champ
                    else:
                        save_shards = 2  # mastery 5 and below champ
                else:
                    save_shards = 2  # (?) mastery 0 - owned, but never touched
            else:
                save_shards = 3  # not owned champ

            disenchant_shards = max(0, item["count"] - save_shards)

            if disenchant_shards:
                disenchant_req = await connection.request(
                    "post",
                    f"/lol-loot/v1/recipes/CHAMPION_RENTAL_disenchant/craft?repeat={disenchant_shards}",
                    data=[item["lootName"]],
                )


def be_mass_disenchant_button():
    connector = AluConnector(worker_func)
    connector.start()


if __name__ == "__main__":
    be_mass_disenchant_button()
