"""
Show skin shards for champions without a skin

## Credits to the orignal source:
* bangingheads gist
https://gist.github.com/bangingheads/e1e5f6aa9ee9ca74d84edc8874d04a59

At some point, I will streamline this script and all other scripts into my whole chore-bulking concept.
"""
from __future__ import annotations

from typing import TYPE_CHECKING

import easygui
import requests

from common.connector import AluConnector

if TYPE_CHECKING:
    from lcu_driver.connection import Connection


async def worker_func(connection: Connection):
    version = requests.get("https://ddragon.leagueoflegends.com/api/versions.json").json()[0]
    ddragon = requests.get(f"https://ddragon.leagueoflegends.com/cdn/{version}/data/en_US/championFull.json").json()
    champs = ddragon["keys"]

    summoner = await connection.request("get", "/lol-summoner/v1/current-summoner")
    summoner = await summoner.json()
    summoner_id = summoner["summonerId"]

    ownership = {champ: {"owned": False, "skins": 0, "unlockable": []} for champ in champs.keys()}

    for champ_id in champs.keys():
        champ_data = await connection.request(
            "get", f"/lol-champions/v1/inventories/{summoner_id}/champions/{champ_id}"
        )
        if champ_data.status != 200:
            continue
        champ_data = await champ_data.json()

        ownership[champ_id]["owned"] = champ_data["ownership"]["owned"]
        if champ_data["ownership"]["owned"]:
            for skin in champ_data["skins"]:
                if skin["ownership"]["owned"] and skin["isBase"] != True:
                    ownership[champ_id]["skins"] += 1

    loots = await connection.request("get", f"/lol-loot/v1/player-loot")
    loots = await loots.json()

    for loot in loots:
        if loot["displayCategories"] == "SKIN":
            champ = str(loot["storeItemId"])[:-3]
            if loot["parentItemStatus"] == "OWNED" and ownership[champ]["skins"] == 0:
                ownership[champ]["unlockable"].append(loot["itemDesc"])

    display = ""
    for key, data in ownership.items():
        if data["owned"] == True and data["skins"] == 0 and len(data["unlockable"]) > 0:
            display += ddragon["data"][ddragon["keys"][key]]["name"] + "\n" + "\n".join(data["unlockable"]) + "\n\n"

    easygui.msgbox(display, title="Champions With 0 Skins That Can Unlock", ok_button="Go Unlock Some Skins!")


def show_zero_skins_shards_button():
    connector = AluConnector(worker_func)
    connector.start()


if __name__ == "__main__":
    show_zero_skins_shards_button()
