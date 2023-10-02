from __future__ import annotations

from typing import TYPE_CHECKING

from src.my_connector import AluConnector

if TYPE_CHECKING:
    from aiohttp import ClientResponse
    from lcu_driver.connection import Connection


async def worker_func(connection: Connection, summoner: ClientResponse) -> None:
    req = await connection.request(
        "post",
        "/lol-challenges/v1/update-player-preferences/",
        data={"challengeIds": []},
    )
    print(f"Req status: {req.status}")


connector = AluConnector(worker_func)
connector.start()
