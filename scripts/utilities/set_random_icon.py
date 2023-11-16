"""Set Random Icon

Sets random icon from your owned icons. 
Frankly, this script exists only for testing purposes as in
I test some interactions here without messing around 
with more complex code from other published scripts.
"""

from __future__ import annotations

import logging
import random

from common.connector import AluConnector

log = logging.getLogger(__name__)


class SetRandomIcon(AluConnector):
    """Set Random Owned Icon.

    This will change your league profile icon to a randomly chosen icon from owned ones.
    
    It will print numerical id of that icon into the console.
    """

    async def callback(self) -> str:
        r_icons = await self.get("/lol-inventory/v2/inventory/SUMMONER_ICON")
        icon_ids = [icon["itemId"] for icon in await r_icons.json()]

        icon_id = random.choice(icon_ids)  # = randint(50, 78) # random_chinese_icon
        r_put = await self.put("/lol-summoner/v1/current-summoner/icon", data={"profileIconId": icon_id})
        if r_put.status == 201:
            result = f"Icon with Id={icon_id} was set correctly."
        else:
            result = "Unknown problem, the icon was not set."
        log.info("%s", result)
        return result


if __name__ == "__main__":
    SetRandomIcon().start()
