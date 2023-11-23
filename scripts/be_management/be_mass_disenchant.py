"""
# Mass-Disenchant Champion Shards accounting for Mastery levels.

- [X] keep 3/2/1/0 champion shards depending on their mastery - 
respectively to not_owned/5_and_below/6/7 level.
- [ ] Disenchant permanent shards for owned champions.
"""

from __future__ import annotations

from typing import Mapping, NamedTuple

from common import AluConnector


class ShardToDisenchant(NamedTuple):
    name: str
    type: str
    count: int


class BEMassDisenchant(AluConnector):
    """Blue Essence Mass Disenchant accounting for Mastery Levels.

    This script disenchants champion shards depending on their mastery level.
    The following logic applies:

    ## Champion Shards (Usual ones)
    * Keep N champion shards untouched respectively for ***:
        * 3 shards - now owned champions
        * 2 shards - mastery 5 and below
        * 1 shard - mastery 6 champions
        * 0 shards - mastery 7 champions
    * Disenchant all other shards.

    ## Permanent champion shards (Golden border ones)
    * Keep 1 shard for unowned champions so you can unlock it.
    * Disenchant the rest since it's more efficient to wait for a usual champion shard to upgrade the mastery with.

    The script will show the list of shards to disenchant and then you will be able to confirm/deny the procedure.
    """

    async def callback(self: AluConnector) -> str:
        r_summoner = await self.get("/lol-summoner/v1/current-summoner")
        summoner_id: int = (await r_summoner.json())["summonerId"]

        # Champion ID - Mastery Level Mapping
        r_mastery = await self.get(f"/lol-collections/v1/inventories/{summoner_id}/champion-mastery")
        champ_id_to_mastery_level: Mapping[int, int] = {
            item["championId"]: item["championLevel"] for item in await r_mastery.json()
        }

        # Loot
        r_loot = await self.get("/lol-loot/v1/player-loot")

        # gather statistics about the shards to disenchant
        shards_to_confirm: list[ShardToDisenchant] = []
        for item in await r_loot.json():
            match item["type"]:
                case "CHAMPION_RENTAL":  # normal "partial" champion shard
                    if item["itemStatus"] == "OWNED":
                        champ_id = item["storeItemId"]
                        mastery_level = champ_id_to_mastery_level.get(champ_id, 0)
                        # 7 level -> 0 shards to save (6 level->1, 5->2, 4->2, 3->2, 2->2, 1->2, 0->2)
                        shards_to_save = min(7 - mastery_level, 2)
                    else:
                        # not owned champ -> 3 shards to save
                        shards_to_save = 3
                case "CHAMPION":  # permanent champion shard
                    shards_to_save = int(item["itemStatus"] != "OWNED")  # don't own -> need to save one shard.
                case _:
                    continue

            shards_to_disenchant = max(0, item["count"] - shards_to_save)

            if shards_to_disenchant:
                shards_to_confirm.append(
                    ShardToDisenchant(
                        name=item["lootName"],
                        type=item["type"],
                        count=shards_to_disenchant,
                    )
                )

        # Confirm
        text = "".join([f"{shard.name} - {shard.type}: {shard.count} shards" for shard in shards_to_confirm])
        if not text:
            text = "No shards to disenchant."
        else:
            text = "The following Champion shards will be disenchanted:\n" + text
        self.confirm(text)

        # We can finally disenchant
        total_shards_disenchanted = 0
        for shard in shards_to_confirm:
            r = await self.post(
                f"/lol-loot/v1/recipes/{shard.type}_disenchant/craft?repeat={shard.count}",
                data=[shard.name],
            )
            if r.status == 201:
                total_shards_disenchanted += shard.count

        return f"Disenchanted {total_shards_disenchanted} shards"


if __name__ == "__main__":
    BEMassDisenchant().start()
