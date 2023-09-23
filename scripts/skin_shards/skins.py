from __future__ import annotations

import pprint
from typing import TYPE_CHECKING, Mapping

import aiohttp
from lcu_driver import Connector

if TYPE_CHECKING:
    from aiohttp import ClientResponse
    from lcu_driver.connection import Connection

connector = Connector()


async def get_skinid_rp_mapping() -> Mapping[int, int | str]:
    """Get mapping `skin_id` -> `price`.
    Just a general relation so we know price of every single skin.

    The information is provided by merakianalytics.com
    Example output:
    >>> {266001: 975, 266002: 1350, ... , 33007: 975, 33008: 975, ...}

    Some skin prices are marked as 'Special' - it usually means the skin comes as
    Prestige/Mythic or some other edge-cases.

    There is also a situation about skins that are not Loot Eligible. Their price marked as 'yNoLootEligible'
    The mapping also includes Upcoming skins.
    """
    skinid_rp_mapping: Mapping[int, int | str] = {}

    url = "https://cdn.merakianalytics.com/riot/lol/resources/latest/en-US/champions.json"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            champ_json = await resp.json()

            for _champ_name, champ_data in champ_json.items():
                for skin in champ_data["skins"]:
                    if skin["isBase"]:
                        continue
                    if not skin["lootEligible"]:
                        skinid_rp_mapping[
                            skin["id"]
                        ] = "yNoLootEligible"  # "y" just so it's after 'Special' in alphabet sort
                    else:
                        skinid_rp_mapping[skin["id"]] = skin["cost"]

    return skinid_rp_mapping


async def get_skinid_owned_mapping(connection: Connection, summoner: ClientResponse) -> Mapping[int, bool]:
    """Get mapping `skin_id` -> `is_owned` so
    we can know what skins I own/do not own.

    Example output:
    >>> {1001: False, 1002: True, ... 101012: True, ...}
    """
    summoner_id: int = (await summoner.json())["summonerId"]

    req = await connection.request("get", f"/lol-champions/v1/inventories/{summoner_id}/skins-minimal")
    skins_minimal_json = await req.json()

    skinid_owned_mapping: Mapping[int, bool] = {
        skin["id"]: skin["ownership"]["owned"] for skin in skins_minimal_json if not skin["isBase"]
    }

    return skinid_owned_mapping


async def worker_func(connection: Connection, summoner: ClientResponse) -> None:
    """Main function of this script.

    Which is to print a dictionary that shows how many skins of each price tier
    I own/do not own.

    This information gets pasted into excel spreadsheet for further and more visually appealing math.

    Example output:
    >>> {390: {'not_owned': 3, 'owned': 0}, ... 'Special': {'not_owned': 67, 'owned': 19}}
    """

    skinid_rp_mapping = await get_skinid_rp_mapping()
    skinid_owned_mapping = await get_skinid_owned_mapping(connection, summoner)

    price_categories = {}  # {k: {"owned": 0, "not_owned": 0} for k in [520, 750, 975, 1350, 1820]}

    for skin_id, is_owned in skinid_owned_mapping.items():
        price = skinid_rp_mapping[skin_id]

        if price not in price_categories:
            price_categories[price] = {"owned": int(is_owned), "not_owned": int(not is_owned)}
        else:
            price_categories[price]["owned"] += int(is_owned)
            price_categories[price]["not_owned"] += int(not is_owned)

    pprint.pprint(price_categories)


@connector.ready
async def connect(connection: Connection):
    print("LCU API is ready to be used.")
    summoner = await connection.request("get", "/lol-summoner/v1/current-summoner")
    if summoner.status != 200:
        print("Please login into your account and restart the script...")
    else:
        await worker_func(connection, summoner)


@connector.close
async def disconnect(_: Connection):
    print("The LCU API client have been closed!")


connector.start()
