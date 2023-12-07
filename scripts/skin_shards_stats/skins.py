from __future__ import annotations

from typing import Any, Mapping

import aiohttp

from common import AluConnector, TabularData


class SkinCollectionStats(AluConnector):
    """Skin Collection Statistics

    This feature will print out how many skins of each price tier you do/don't own.

    Nerdy statistic that can be used in some Excel calculations about efficient skin collection grind.

    The script will output a table with price categories which are
    * RP prices ranging from 390 RP till 3250 RP
    * Not Loot Eligible skins
    * Special Price skins which are mostly Event skins, Mythic Essence skins, Prestige skins.
    * Unknown Price skins which unfortunately we couldn't get the price data about.
    """

    def __init__(self, need_confirmation: bool = False):
        super().__init__(need_confirmation)
        self.skins_minimal: list[dict[str, Any]] = []

    async def callback(self) -> str:
        await self.set_skins_minimal()
        price_by_skin_id = await self.get_price_by_skin_id()
        is_owned_by_skin_id = await self.get_is_owned_by_skin_id()

        price_categories = {}

        no_price_data_skins: list[int] = []

        for skin_id, is_owned in is_owned_by_skin_id.items():
            price = price_by_skin_id.get(skin_id, None)
            if not price:
                # most likely some meraki json problem
                # i.e. when Hwei data was not available 2 days after his release
                price = "Unknown"
                no_price_data_skins.append(skin_id)

            if price not in price_categories:
                price_categories[price] = {"owned": int(is_owned), "not_owned": int(not is_owned)}
            else:
                price_categories[price]["owned"] += int(is_owned)
                price_categories[price]["not_owned"] += int(not is_owned)

        table = TabularData()
        table.set_columns(["Price", "NotOwned", "Owned"])
        for price in sorted(price_categories.keys(), key=lambda x: (not x.isnumeric(), int(x) if x.isnumeric() else x)):
            price_dict = price_categories[price]
            table.add_row([price, price_dict["not_owned"], price_dict["owned"]])

        text = f"Statistics about your skin collection:\n{table.render()}"
        if no_price_data_skins:
            text += "\n\nThe skins under 'Unknown Price' category are:\n"
            name_by_skin_id = await self.get_name_by_skin_id()
            text += "\n".join([f"* {name_by_skin_id[id_]}" for id_ in no_price_data_skins])
        self.output(text)
        return "Success: Statistic was shown."

    # MERAKI CDN

    async def get_price_by_skin_id(self) -> Mapping[int, str]:
        """Get mapping `skin_id` -> `price in RP`.
        So we know general price stats about all league skins.

        The information is provided by merakianalytics.com
        Example output:
        >>> {266001: 975, 266002: 1350, ... , 33007: 975, 33008: 975, ...}

        Some skin prices are marked as 'Special' - it usually means the skin comes as
        Prestige/Mythic or some other edge-cases.

        There is also a situation about skins that are not Loot Eligible. Their price marked as 'NoLootEligible'
        The mapping also includes Upcoming skins.
        """

        price_by_skin_id: Mapping[int, str] = {}

        url = "https://cdn.merakianalytics.com/riot/lol/resources/latest/en-US/champions.json"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                champ_json = await resp.json()

        # print([i["name"] for i in champ_json["Camille"]["skins"]])
        # print(champ_json.keys())

        for champ_data in champ_json.values():
            for skin in champ_data["skins"]:
                if skin["isBase"]:
                    continue

                if not skin["lootEligible"]:
                    price_by_skin_id[skin["id"]] = "NoLootEligible"
                else:
                    price_by_skin_id[skin["id"]] = str(skin["cost"])

        return price_by_skin_id

    # LCU API PART
    async def set_skins_minimal(self) -> None:
        """Get skins minimal dict from LCU API.

        Used to make mappings is_owned_by_skin_id, name_by_skin_id, ...
        """
        r_summoner = await self.get("/lol-summoner/v1/current-summoner")
        summoner_id: int = (await r_summoner.json())["summonerId"]

        r_skins = await self.get(f"/lol-champions/v1/inventories/{summoner_id}/skins-minimal")
        self.skins_minimal = await r_skins.json()

    async def get_is_owned_by_skin_id(self) -> Mapping[int, bool]:
        """Get mapping `skin_id` -> `is_owned`
        So we can know what skins we own/do not own.

        Example output:
        >>> {1001: False, 1002: True, ... 101012: True, ...}
        """

        return {skin["id"]: skin["ownership"]["owned"] for skin in self.skins_minimal if not skin["isBase"]}

    async def get_name_by_skin_id(self) -> Mapping[int, str]:
        """Get mapping `skin_id` -> `skin_name`
        So we can know what skins we own/do not own.

        Example output:
        >>> {1001: 'Goth Annie', 1002: 'Red Riding Annie', ... 950001: 'Soul Fighter Naafiri', ...}
        """

        return {skin["id"]: skin["name"] for skin in self.skins_minimal if not skin["isBase"]}


if __name__ == "__main__":
    SkinCollectionStats().start()
