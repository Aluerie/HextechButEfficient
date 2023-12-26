"""
This is a bit over-cooking typing in pursue of Wrapper-like typing :D
Might be outdated in no time though too.
"""

from __future__ import annotations

from typing import Optional, TypedDict

# fmt: off
# I just want #'s to be aligned nicely

# GET /lol-champions/v1/inventories/{summoner_id}/skins-minimal
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
    splashPath: str                 # "/lol-game-data/assets/v1/champion-splashes/1/1000.jpg"
    stillObtainable: bool
    tilePath: str                   # "/lol-game-data/assets/v1/champion-tiles/1/1000.jpg"


# /lol-loot/v1/player-loot
class LootItem(TypedDict):
    asset: str                      # ""
    count: int                      # 1
    disenchantLootName: str         # "CURRENCY_cosmetic",
    disenchantRecipeName: str       # "SKIN_RENTAL_disenchant",
    disenchantValue: int            # 364,
    displayCategories: str          # "SKIN", #TODO: maybe literal on this?
    expiryTime: int                 # -1,
    isNew: bool                     # False
    isRental: bool                  # True
    itemDesc: str                   # "Dragon Trainer Heimerdinger",
    itemStatus: str                 # "NONE", #TODO: maybe literal on this?
    localizedDescription: str       # "",
    localizedName: str              # "",
    localizedRecipeSubtitle: str    # "",
    localizedRecipeTitle: str       # "",
    lootId: str                     # "CHAMPION_SKIN_RENTAL_74006",
    lootName: str                   # "CHAMPION_SKIN_RENTAL_74006",
    parentItemStatus: str           # "OWNED", #TODO: maybe literal on this?
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
    type: str                       # "SKIN_RENTAL", #TODO: maybe literal on this?
    upgradeEssenceName: str         # "CURRENCY_cosmetic"
    upgradeEssenceValue: int        # 1520
    upgradeLootName: str            # "CHAMPION_SKIN_74006"
    value: int                      # 1820


# f"/lol-collections/v1/inventories/{self.summoner_id}/champion-mastery"
class ChampionMastery(TypedDict):
    championId: int                             # 16,
    championLevel: int                          # 7,
    championPoints: int                         # 546475,
    championPointsSinceLastLevel: int           # 524875,
    championPointsUntilNextLevel: int           # 0,
    chestGranted: bool                          # True,
    formattedChampionPoints: str                # "546,475",
    formattedMasteryGoal: str                   # "546,475",
    highestGrade: str                           # "S+",
    lastPlayTime: int                           # 1693938829000,
    playerId: int                               # 0,
    puuid: str                                  # "ef550652-6f19-508f-b6bd-00886efde891",
    tokensEarned: int                           # 0,


# /lol-summoner/v1/current-summoner
class RerollPoints(TypedDict):
    currentPoints: int          # 500,
    maxRolls: int               # 2,
    numberOfRolls: int          # 2,
    pointsCostToRoll: int       # 250,
    pointsToReroll: int         # 0,


class CurrentSummoner(TypedDict):
    accountId: int                      # 1995474734002688,
    displayName: str                    # "Aluerie",
    gameName: str                       # "Aluerie",
    internalName: str                   # "Aluerie",
    nameChangeFlag: bool                # False,
    percentCompleteForNextLevel: int    # 77,
    privacy: str                        # "PUBLIC",
    profileIconId: int                  # 5914,
    puuid: str                          # "ef550652-6f19-508f-b6bd-00886efde891",
    rerollPoints: RerollPoints
    summonerId: int                     # 114548842,
    summonerLevel: int                  # 599,
    tagLine: str                        # "Alu",
    unnamed: bool                       # False,
    xpSinceLastLevel: int               # 2822,
    xpUntilNextLevel: int               # 3648,


# fmt: on
