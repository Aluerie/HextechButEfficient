from __future__ import annotations

from typing import Mapping, NamedTuple

from common import AluConnector, TabularData


class ShardToDisenchant(NamedTuple):
    type: str
    loot_id: str
    count: int
    display_name: str
    disenchant_value: int


class BaseBEDisenchant(AluConnector):
    """Base class for BE disenchant operations.

    Subclasses of this should implement `get_shards_to_confirm`.
    """

    async def get_shards_to_confirm(self) -> list[ShardToDisenchant]:
        """Get list of shards to disenchant with detailed statistic

        This function should describe the strategy of mass-disenchanting, i.e.
        it should account for mastery level, or
        it should include everything, etc.
        """
        ...

    async def callback(self) -> str:
        shards_to_confirm = await self.get_shards_to_confirm()

        # Confirm
        if not shards_to_confirm:
            text = "No shards to disenchant."
            self.output(text)
        else:
            text = "The following Champion shards will be disenchanted:\n"
            table = TabularData()
            table.set_columns(["Shard Name", "Amount", "BE Value"])
            rows = [(shard.display_name, shard.count, shard.disenchant_value) for shard in shards_to_confirm]
            table.add_rows(rows)
            text += table.render()
            total_be = sum(shard.disenchant_value * shard.count for shard in shards_to_confirm)
            text += f"\nTotal Amount of Blue Essence to gain: {total_be}"

            self.confirm(text)

        # We can finally disenchant
        total_shards_disenchanted = 0
        for shard in shards_to_confirm:
            r = await self.post(
                f"/lol-loot/v1/recipes/{shard.type}_disenchant/craft?repeat={shard.count}",
                data=[shard.loot_id],
            )
            if r.ok:
                total_shards_disenchanted += shard.count

        return f"Disenchanted {total_shards_disenchanted} shards"


class BEMassDisenchant(BaseBEDisenchant):
    """Blue Essence Mass Disenchant accounting for Mastery Levels.

    This script disenchants champion shards depending on their mastery level.
    The motivation is that long-term it's better to upgrade the champion mastery with Basic Champion Shard option over 2400 BE/Permanent.
    Thus, we keep just enough shards to upgrade mastery/unlock champions and disenchant the rest.
    In details, the following logic applies:

    ## Champion Shards (Usual ones)
    * Keep N champion shards untouched respectively for ***:
        * 3 shards - not owned champions
        * 2 shards - mastery 5 and below
        * 1 shard - mastery 6 champions
        * 0 shards - mastery 7 champions
    * Disenchant all other shards.

    ## Permanent champion shards (Golden border ones)
    * Keep 1 shard for unowned champions so you can unlock it.
    * Disenchant the rest since it's more efficient to wait for a usual champion shard to upgrade the mastery with.

    The script will show the list of shards to disenchant and then you will be able to confirm/deny the procedure.
    """

    async def get_shards_to_confirm(self) -> list[ShardToDisenchant]:
        # Champion ID - Mastery Level Mapping
        r_summoner = await self.get("/lol-summoner/v1/current-summoner")
        summoner_id: int = (await r_summoner.json())["summonerId"]

        r_mastery = await self.get(f"/lol-collections/v1/inventories/{summoner_id}/champion-mastery")
        champ_id_to_mastery_level: Mapping[int, int] = {
            item["championId"]: item["championLevel"] for item in await r_mastery.json()
        }

        # Loot
        r_loot = await self.get("/lol-loot/v1/player-loot")

        shards_to_confirm: list[ShardToDisenchant] = []
        for item in await r_loot.json():
            match item["type"]:
                case "CHAMPION_RENTAL":  # normal "partial" champion shard
                    extra_display_text = ""
                    if item["itemStatus"] == "OWNED":
                        champ_id = item["storeItemId"]
                        mastery_level = champ_id_to_mastery_level.get(champ_id, 0)
                        # 7 level -> 0 shards to save (6 level->1, 5->2, 4->2, 3->2, 2->2, 1->2, 0->2)
                        shards_to_save = min(7 - mastery_level, 2)
                    else:
                        # not owned champ -> 3 shards to save
                        shards_to_save = 3
                case "CHAMPION":  # permanent champion shard
                    extra_display_text = " Permanent"
                    shards_to_save = int(item["itemStatus"] != "OWNED")  # don't own -> need to save one shard.
                case _:
                    continue

            shards_to_disenchant = max(0, item["count"] - shards_to_save)

            if shards_to_disenchant:
                shards_to_confirm.append(
                    ShardToDisenchant(
                        type=item["type"],
                        loot_id=item["lootId"],
                        count=shards_to_disenchant,
                        display_name=item["itemDesc"] + extra_display_text,
                        disenchant_value=item["disenchantValue"],
                    )
                )
        return shards_to_confirm


if __name__ == "__main__":
    BEMassDisenchant().start()


""" 
A scheme of item in 
"for item in await r_loot.json():"
case "CHAMPION_RENTAL"

Just so I don't need to do extra print(item) when I want to change something.
{
    "asset": "",
    "count": 1,
    "disenchantLootName": "CURRENCY_champion",
    "disenchantRecipeName": "CHAMPION_RENTAL_disenchant",
    "disenchantValue": 960,
    "displayCategories": "CHAMPION",
    "expiryTime": -1,
    "isNew": False,
    "isRental": True,
    "itemDesc": "Kayle",  # /* cspell: disable-line */
    "itemStatus": "OWNED",
    "localizedDescription": "",
    "localizedName": "",
    "localizedRecipeSubtitle": "",
    "localizedRecipeTitle": "",
    "lootId": "CHAMPION_RENTAL_10",
    "lootName": "CHAMPION_RENTAL_10",
    "parentItemStatus": "NONE",
    "parentStoreItemId": -1,
    "rarity": "DEFAULT",
    "redeemableStatus": "ALREADY_OWNED",
    "refId": "",
    "rentalGames": 0,
    "rentalSeconds": 604800,
    "shadowPath": "",
    "splashPath": "/lol-game-data/assets/v1/champion-splashes/10/10000.jpg",
    "storeItemId": 10,
    "tags": "",
    "tilePath": "/lol-game-data/assets/v1/champion-tiles/10/10000.jpg",
    "type": "CHAMPION_RENTAL",
    "upgradeEssenceName": "CURRENCY_champion",
    "upgradeEssenceValue": 2880,
    "upgradeLootName": "CHAMPION_10",
    "value": 4800,
}
"""
