from __future__ import annotations

from typing import TYPE_CHECKING

from common.connector import AluConnector

if TYPE_CHECKING:
    from lcu_driver.connection import Connection


async def worker_func(connection: Connection) -> None:
    req = await connection.request(
        "post",
        "/lol-challenges/v1/update-player-preferences/",
        data={"challengeIds": []},
    )
    print(f"Req status: {req.status}")


def remove_challenges_tokens_button():
    connector = AluConnector(worker_func)
    connector.start()


if __name__ == "__main__":
    remove_challenges_tokens_button()
