from __future__ import annotations

import pprint
from typing import Mapping

import aiohttp

from common import AluConnector


class SkinCollectionStats(AluConnector):
    """Skin Collection Statistics

    This feature will print out how many skins of each price tier you do/don't own.

    Nerdy statistic that can be used in some Excel calculations about efficient skin collection grind.

    Example output:
    {390: {'not_owned': 3, 'owned': 0}, ... ,
     1820: {'not_owned': 67, 'owned': 19}, ... ,
     'Special': {'not_owned': 67, 'owned': 19}}
    """

    async def callback(self) -> str:
        skinid_rp_mapping = await self.get_skin_to_rp_mapping()
        skinid_owned_mapping = await self.get_skinid_owned_mapping()

        price_categories = {}

        for skin_id, is_owned in skinid_owned_mapping.items():
            price = skinid_rp_mapping[skin_id]

            if price not in price_categories:
                price_categories[price] = {"owned": int(is_owned), "not_owned": int(not is_owned)}
            else:
                price_categories[price]["owned"] += int(is_owned)
                price_categories[price]["not_owned"] += int(not is_owned)

        # pprint.pprint(price_categories)
        self.output(f"Statistics about your skin collection:\n{pprint.pformat(price_categories)}")
        return "Success: Statistic was shown."

    async def get_skin_to_rp_mapping(self) -> Mapping[int, int | str]:
        """Get mapping `skin_id` -> `price in RP`.
        So we know general price stats about all league skins.

        The information is provided by merakianalytics.com
        Example output:
        >>> {266001: 975, 266002: 1350, ... , 33007: 975, 33008: 975, ...}

        Some skin prices are marked as 'Special' - it usually means the skin comes as
        Prestige/Mythic or some other edge-cases.

        There is also a situation about skins that are not Loot Eligible. Their price marked as 'yNoLootEligible'
        The mapping also includes Upcoming skins.
        """
        skin_to_rp: Mapping[int, int | str] = {}

        url = "https://cdn.merakianalytics.com/riot/lol/resources/latest/en-US/champions.json"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                champ_json = await resp.json()

        for champ_data in champ_json.values():
            for skin in champ_data["skins"]:
                if skin["isBase"]:
                    continue

                if not skin["lootEligible"]:
                    # "yNoLootEligible" - "y" just so it's after 'Special' in alphabet sort
                    skin_to_rp[skin["id"]] = "yNoLootEligible"
                else:
                    skin_to_rp[skin["id"]] = skin["cost"]

        return skin_to_rp

    async def get_skinid_owned_mapping(self) -> Mapping[int, bool]:
        """Get mapping `skin_id` -> `is_owned`
        So we can know what skins we own/do not own.

        Example output:
        >>> {1001: False, 1002: True, ... 101012: True, ...}
        """
        r_summoner = await self.get("/lol-summoner/v1/current-summoner")
        summoner_id: int = (await r_summoner.json())["summonerId"]

        r_skins = await self.get(f"/lol-champions/v1/inventories/{summoner_id}/skins-minimal")
        skins_minimal = await r_skins.json()

        skin_id_to_is_owned: Mapping[int, bool] = {
            skin["id"]: skin["ownership"]["owned"] for skin in skins_minimal if not skin["isBase"]
        }

        return skin_id_to_is_owned


if __name__ == "__main__":
    SkinCollectionStats().start()
