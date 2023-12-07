from __future__ import annotations

from typing import Mapping, NamedTuple

import aiohttp

from common import AluConnector

__all__ = ("BEMassOpening",)


class ChestToOpen(NamedTuple):
    loot_id: str
    count: int
    display_name: str


async def get_be_mass_opening_dict() -> Mapping[str, str]:
    """Get mapping of "loot_id -> localised name" for BE related loot.

    Information is taken from community dragon.
    """
    # we could use
    # https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/loot.json
    # for the whole loot, but it is 100k+ lines of json :D
    # this is why we just use the translation json

    url = "https://raw.communitydragon.org/latest/plugins/rcp-fe-lol-loot/global/en_us/trans.json"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            trans_json: Mapping[str, str] = await resp.json()

    be_chest_dict: Mapping[str, str] = {}

    # THIS PART IS SCARY
    loot_names_to_look_for = (
        "Champion Capsule",
        "Basic Champion Capsule",
        "Glorious Champion Capsule",
        "Honor Level 3 Orb",
        "Honor Level 4 Orb",
        "Honor Level 5 Orb",
        "Honor Level 3 Capsule",
        "Honor Level 4 Capsule",
        "Honor Level 5 Capsule",
        "Hextech Mystery Champion",
    )

    for loot_string, translation in trans_json.items():
        if not loot_string.startswith("loot_name_chest"):
            continue
        elif any([word in translation for word in loot_names_to_look_for]):
            loot_id = loot_string.replace("loot_name_", "").upper()

            be_chest_dict[loot_id] = translation

    return be_chest_dict


class BEMassOpening(AluConnector):
    """Blue Essence Loot Mass Opening

    This opens the following BE related loot:
    * Basic Champion Capsules
    * Glorious Champion Capsules
    * Honour Level 3, 4, 5 Orbs
    * Honour Level 3, 4, 5 Capsules
    * Hextech Mystery Champion

    Permanent Champion Shards will not be touched because it's better to open them manually when new champions get released since it will just give a random unowned champion

    The script will show confirmation prompt with a list of chests to open.
    """

    async def callback(self: AluConnector) -> str:
        be_chest_dict = await get_be_mass_opening_dict()

        r_loot = await self.get("/lol-loot/v1/player-loot")

        chests_to_open: list[ChestToOpen] = []
        for item in await r_loot.json():
            if item["lootId"] in be_chest_dict.keys():
                chests_to_open.append(
                    ChestToOpen(
                        loot_id=item["lootId"],
                        count=item["count"],
                        display_name=be_chest_dict[item["lootId"]],
                    )
                )

        # Confirm
        text = "\n".join([f"{chest.display_name} - x{chest.count}" for chest in chests_to_open])
        if not text:
            text = "No chests to open"
        else:
            text = "The Following Chests will be opened:\n" f"{text}"
        self.confirm(text)

        total_chests_opened = 0
        for chest in chests_to_open:
            r = await self.post(
                f"/lol-loot/v1/recipes/{chest.loot_id}_OPEN/craft?repeat={chest.count}",
                data=[chest.loot_id],
            )
            if r.ok:
                total_chests_opened += chest.count

        return f"Opened {total_chests_opened} chests"


if __name__ == "__main__":
    BEMassOpening().start()


"""
The Schema of chests dictionary

This is Glorious Champion capsule. And unfortunately everything is empty except 'CHEST_129'
So not really helpful, can't even get to know what is what without experiments.
So I guess gotta use community dragon resources.
{
    "asset": "",
    "count": 2,
    "disenchantLootName": "",
    "disenchantRecipeName": "",
    "disenchantValue": 0,
    "displayCategories": "CHEST",
    "expiryTime": -1,
    "isNew": False,
    "isRental": False,
    "itemDesc": "",
    "itemStatus": "NONE",
    "localizedDescription": "",
    "localizedName": "",
    "localizedRecipeSubtitle": "",
    "localizedRecipeTitle": "",
    "lootId": "CHEST_129",
    "lootName": "CHEST_129",
    "parentItemStatus": "NONE",
    "parentStoreItemId": -1,
    "rarity": "DEFAULT",
    "redeemableStatus": "NOT_REDEEMABLE",
    "refId": "",
    "rentalGames": 0,
    "rentalSeconds": 0,
    "shadowPath": "",
    "splashPath": "/fe/lol-loot/assets/loot_item_icons/chest_129.png",
    "storeItemId": 129,
    "tags": "",
    "tilePath": "/fe/lol-loot/assets/loot_item_icons/chest_129.png",
    "type": "CHEST",
    "upgradeEssenceName": "",
    "upgradeEssenceValue": 0,
    "upgradeLootName": "",
    "value": 0,
}
"""
