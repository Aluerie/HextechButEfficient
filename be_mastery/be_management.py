from __future__ import annotations
from typing import TYPE_CHECKING, TypedDict

from lcu_driver import Connector

if TYPE_CHECKING:
    from lcu_driver.connection import Connection

connector = Connector()


class ChampData(TypedDict):
    name: str
    level: int
    tokens_earned: int
    owned: bool
    shards: int
    full_shards: int


@connector.ready
async def connect(connection: Connection):
    print('LCU API is ready to be used.')
    summoner = await connection.request('get', '/lol-summoner/v1/current-summoner')
    if summoner.status != 200:
        print('Please login into your account to change your icon and restart the script...')
    else:
        summoner_id: int = (await summoner.json())['summonerId']

        req = await connection.request('get', f'/lol-champions/v1/inventories/{summoner_id}/champions')
        champ_dict: dict[int, ChampData] = {  # champ_ownership
            item['id']: {
                'name': item['alias'],
                'owned': item['ownership']['owned']
            } for item in await req.json()
        }

        req = await connection.request('get', f'/lol-collections/v1/inventories/{summoner_id}/champion-mastery')
        for item in await req.json():
            d = champ_dict[item['championId']]
            d['level'] = item['championLevel']
            d['tokens_earned'] = item['tokensEarned']

        req = await connection.request('get', '/lol-loot/v1/player-loot')
        for item in await req.json():
            if item["type"] == "CHAMPION_RENTAL":
                d = champ_dict[item['storeItemId']]
                d['shards'] = item['count']

        print([{k: v} for k, v in champ_dict.items() if v.get('shards', 0)])



        # print(champ_shards)

        # req = await connection.request(
        #     'post', '/lol-loot/v1/recipes/CHAMPION_RENTAL_disenchant/craft?repeat=1',
        #     data=["CHAMPION_RENTAL_20"]
        # )
        # ctx_menu = await req.json()
        # print(ctx_menu)

        req = await connection.request('get', '/swagger/v1/api-docs')
        d = await req.json()
        print(d)


@connector.close
async def disconnect(_: Connection):
    print('The client have been closed!')


connector.start()
