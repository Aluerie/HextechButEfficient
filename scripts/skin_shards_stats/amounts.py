from __future__ import annotations

from typing import TYPE_CHECKING, Any, Mapping, Optional, TypedDict

import aiohttp

from common import AluConnector, TabularData

if TYPE_CHECKING:
    # Somewhat unnecessary over cooked type-hinting
    # might be outdated in no time too
    # last updated 26 December 2023

    # /lol-champions/v1/inventories/{summoner_id}/skins-minimal
    class Rental(TypedDict):
        endDate: int
        purchaseDate: int
        rented: bool
        winCountRemaining: int

    class Ownership(TypedDict):
        loyaltyReward: bool
        owned: bool
        rental: Rental
        xboxGPReward: bool

    class MinimalSkin(TypedDict):
        championId: int
        chromaPath: Optional[str]
        disabled: bool
        id: int
        isBase: bool
        lastSelected: bool
        name: str
        ownership: Ownership
        splashPath: str  # "/lol-game-data/assets/v1/champion-splashes/1/1000.jpg"
        stillObtainable: bool
        tilePath: str  # "/lol-game-data/assets/v1/champion-tiles/1/1000.jpg"

    # "/lol-loot/v1/player-loot" - ["displayCategories"] == "SKIN"
    # fmt: off
    class LootSkin(TypedDict):
        asset: str                      # ""
        count: int                      # 1
        disenchantLootName: str         # "CURRENCY_cosmetic",
        disenchantRecipeName: str       # "SKIN_RENTAL_disenchant",
        disenchantValue: int            # 364,
        displayCategories: int          # "SKIN",
        expiryTime: int                 # -1,
        isNew: bool                     # False
        isRental: bool                  # True
        itemDesc: str                   # "Dragon Trainer Heimerdinger",
        itemStatus: str                 # "NONE",
        localizedDescription: str       # "",
        localizedName: str              # "",
        localizedRecipeSubtitle: str    # "",
        localizedRecipeTitle: str       # "",
        lootId: str                     # "CHAMPION_SKIN_RENTAL_74006",
        lootName: str                   # "CHAMPION_SKIN_RENTAL_74006",
        parentItemStatus: str           # "OWNED",
        parentStoreItemId: int          # 74,
        rarity: str                     # "LEGENDARY",
        redeemableStatus: str           # "REDEEMABLE_RENTAL",
        refId: str                      # "",
        rentalGames: int                # 0,
        rentalSeconds: int              # 604800,
        shadowPath: str                 # "",
        splashPath: str                 # "/lol-game-data/assets/v1/champion-splashes/74/74006.jpg",
        storeItemId: int                # 74006,
        tags: str                       # "Mage,Mid,Top,legacy,piltover,rarity_legendary"
        tilePath: str                   # "/lol-game-data/assets/v1/champion-tiles/74/74006.jpg"
        type: str                       # "SKIN_RENTAL",
        upgradeEssenceName: str         # "CURRENCY_cosmetic"
        upgradeEssenceValue: int        # 1520
        upgradeLootName: str            # "CHAMPION_SKIN_74006"
        value: int                      # 1820
    # fmt: on

    # my own table dict
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
        r_summoner = await self.get("/lol-summoner/v1/current-summoner")
        summoner_id: int = (await r_summoner.json())["summonerId"]
        r_skins = await self.get(f"/lol-champions/v1/inventories/{summoner_id}/skins-minimal")
        skins_minimal: list[MinimalSkin] = await r_skins.json()

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
        r_loot = await self.get("/lol-loot/v1/player-loot")
        for loot in await r_loot.json():
            if loot["displayCategories"] == "SKIN":
                loot: LootSkin
                champion_id = loot["parentStoreItemId"]
                table_dict[champion_id]["unowned_skin_shards"] += int(loot["itemStatus"] != "OWNED")

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
