from __future__ import annotations

import pprint

from common import AluConnector


class SkinShardsStats(AluConnector):
    """Skin Shards From Loot Statistics

    This feature will print out how many skins shards of each price tier you do/don't own.

    Nerdy statistic that can be used in some Excel calculations about efficient skin collection grind.

    Example output:
    {520: {'not_owned': 3, 'owned': 0}, ... ,
     1820: {'not_owned': 67, 'owned': 19}}
    """

    async def callback(self) -> str:
        r = await self.get("/lol-loot/v1/player-loot")
        player_loot: dict = await r.json()

        skin_shards = [item for item in player_loot if item["displayCategories"] == "SKIN"]

        # todo: it will fail if we have shard price out of these ranged
        shard_categories = {k: {"owned": 0, "not_owned": 0} for k in [520, 750, 975, 1350, 1820]}

        for shard in skin_shards:
            if shard["itemStatus"] == "OWNED":
                shard_categories[shard["value"]]["owned"] += shard["count"]
            else:
                shard_categories[shard["value"]]["not_owned"] += 1
                shard_categories[shard["value"]]["owned"] += shard["count"] - 1

        return f"Statistics about your skin shards in the loot tab:\n{pprint.pformat(shard_categories)}"


if __name__ == "__main__":
    SkinShardsStats().start()
