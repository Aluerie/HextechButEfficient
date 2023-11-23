"""
## Credits to the orignal source:
* bangingheads gist
https://gist.github.com/bangingheads/e1e5f6aa9ee9ca74d84edc8874d04a59
"""
from __future__ import annotations

import aiohttp

from common import AluConnector
from common.constants import URL


class ZeroSkinShards(AluConnector):
    """Show owned skin shards for champions without a skin.

    In other words, show champions with currently 0 owned skins, but you can unlock such with skin shards in the Loot Tab.

    This will not upgrade the skin(-s) shards automatically but just show a list of those in a separate dialog.
    """

    async def callback(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{URL.DDRAGON}/api/versions.json") as response:
                version = (await response.json())[0]

            async with session.get(f"{URL.DDRAGON}/cdn/{version}/data/en_US/championFull.json") as response:
                ddragon = await response.json()
                champs = ddragon["keys"]

        r_summoner = await self.get("/lol-summoner/v1/current-summoner")
        summoner_id = (await r_summoner.json())["summonerId"]

        ownership = {champ: {"owned": False, "skins": 0, "unlockable": []} for champ in champs.keys()}

        for champ_id in champs.keys():
            r_champ_data = await self.get(f"/lol-champions/v1/inventories/{summoner_id}/champions/{champ_id}")
            if r_champ_data.status != 200:
                continue
            champ_data = await r_champ_data.json()

            ownership[champ_id]["owned"] = champ_data["ownership"]["owned"]
            if champ_data["ownership"]["owned"]:
                for skin in champ_data["skins"]:
                    if skin["ownership"]["owned"] and skin["isBase"] != True:
                        ownership[champ_id]["skins"] += 1

        r_loots = await self.get("/lol-loot/v1/player-loot")
        for loot in await r_loots.json():
            if loot["displayCategories"] == "SKIN":
                champ = str(loot["storeItemId"])[:-3]
                if loot["parentItemStatus"] == "OWNED" and ownership[champ]["skins"] == 0:
                    ownership[champ]["unlockable"].append(loot["itemDesc"])

        display = ""
        amount_of_skins = 0
        for key, data in ownership.items():
            if data["owned"] == True and data["skins"] == 0 and len(data["unlockable"]) > 0:
                display += ddragon["data"][ddragon["keys"][key]]["name"] + "\n" + "\n".join(data["unlockable"]) + "\n\n"
                amount_of_skins += len(data["unlockable"])

        if not display:
            display = (
                "Did not find any skin shards which "
                "would be the very first skin for their champion in your collection after upgrading."
            )

        self.output(display)
        return f"Found {amount_of_skins} such skins"


if __name__ == "__main__":
    ZeroSkinShards().start()
