from __future__ import annotations

from typing import TYPE_CHECKING, TypedDict

from common import AluConnector, TabularData

if TYPE_CHECKING:

    class ShardCategory(TypedDict):
        owned: int
        not_owned: int


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

        shard_prices = [shard["value"] for shard in skin_shards]
        shard_categories: dict[int, ShardCategory] = {k: {"owned": 0, "not_owned": 0} for k in shard_prices}

        for shard in skin_shards:
            if shard["itemStatus"] == "OWNED":
                shard_categories[shard["value"]]["owned"] += shard["count"]
            else:
                shard_categories[shard["value"]]["not_owned"] += 1
                shard_categories[shard["value"]]["owned"] += shard["count"] - 1

        table = TabularData()
        table.set_columns(["Price", "NotOwned", "Owned"])
        for price in sorted(shard_categories):
            category = shard_categories[price]
            row = [str(price), category['not_owned'], category["owned"]]
            table.add_row(row)
        self.output(f"Statistics about your skin shards in the loot tab:\n{table.render()}")
        return "Success: Statistic was shown."


if __name__ == "__main__":
    SkinShardsStats().start()
