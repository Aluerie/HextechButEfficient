from __future__ import annotations

from typing import TYPE_CHECKING, TypedDict

from common import AluConnector, TabularData

if TYPE_CHECKING:

    class ChampionDict(TypedDict):
        name: str
        skins_amount: int
        unowned_skin_shards: int


__all__ = ("ChampionSkinAmountStats",)


class ChampionSkinAmountStats(AluConnector):
    """Show Statistics Champion - Amount of Owned Skins

    There are two challenges
    * That Drip - Collect many skins for a champion
    * Need A Bigger Closet - Collect 5 or more skins for a champion
    but there is no way to see how many skins you have per champion.
    For example, what if I have 4 skins + unowned skin shards just enough to get the challenge done after upgrading those.
    Then I have no way of knowing those.
    Personally, I don't even know what champion is presented in "That Drip" challenge for me without this script.
    """

    async def callback(self) -> str:
        # skins data
        skins_minimal = await self.get_lol_champions_v1_inventories_skins_minimal()

        table_dict: dict[int, ChampionDict] = {}
        for skin in skins_minimal:
            champion_id = skin["championId"]

            if champion_id not in table_dict:
                table_dict[champion_id] = {
                    "name": "Unknown Champion",
                    "skins_amount": 0,
                    "unowned_skin_shards": 0,
                }

            if skin["isBase"]:
                table_dict[champion_id]["name"] = skin["name"]
            else:
                table_dict[champion_id]["skins_amount"] += int(skin["ownership"]["owned"])

        # loot data
        for item in await self.get_lol_loot_v1_player_loot():
            if item["displayCategories"] == "SKIN":
                champion_id = item["parentStoreItemId"]
                table_dict[champion_id]["unowned_skin_shards"] += int(item["itemStatus"] != "OWNED")

        # sort by amount of skins
        table_dict = {
            k: v for k, v in sorted(table_dict.items(), key=lambda item: item[1]["skins_amount"], reverse=True)
        }

        # output
        table = TabularData()
        table.set_columns(["Champion", "Skins", "Shards", "Total"])
        for champion_id, champion_dict in table_dict.items():
            total = champion_dict["skins_amount"] + champion_dict["unowned_skin_shards"]
            row = list(champion_dict.values()) + [total]
            table.add_row(row)

        output_text = f"Statistics Champion - Amount of Skins - Amount of Unknown Skin Shards:\n{table.render()}"
        self.output(output_text)
        return "Statistic Champion - Amount of skins was shown"


if __name__ == "__main__":
    ChampionSkinAmountStats().start()
