from __future__ import annotations

import pprint

from common import AluConnector


class SkinShardsStats(AluConnector):
    async def callback(self) -> str:
        """Print a dictionary that shows how many skin shards of each price tier
        I own/do not own.

        This information gets pasted into excel spreadsheet for further and more visually appealing math.
        Example output:
        >>> {520: {'not_owned': 3, 'owned': 0}, ... 1820: {'not_owned': 67, 'owned': 19}}
        """

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

        return f'Statistics about your skin shards in the loot tab:\n{pprint.pformat(shard_categories)}'


if __name__ == "__main__":
    SkinShardsStats().start()
