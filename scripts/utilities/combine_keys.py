from __future__ import annotations

from common import AluConnector


class CombineFragmentKeys(AluConnector):
    """Combine Fragment Keys into full Keys.

    This script will try to combine all possible fragments, i.e. if you have 28 fragments - the script will combine 27 of those into 9 full keys.
    """

    async def callback(self: AluConnector) -> str:
        r_loot = await self.get("/lol-loot/v1/player-loot")
        loot = await r_loot.json()

        for item in loot:
            if item["lootId"] != "MATERIAL_key_fragment":
                continue
            if repeat := item["count"] // 3:
                r_craft = await self.post(
                    f"/lol-loot/v1/recipes/MATERIAL_key_fragment_forge/craft?repeat={repeat}",
                    data=["MATERIAL_key_fragment"],  # data=[item["lootId"]]
                )

                if r_craft.status == 200:
                    return f"Successfully combined {repeat} keys"
                else:
                    return f"Failed to combine keys with {r_craft.status} status"
            else:
                return f"You have less than 3 key fragments to combine"

        return "Did not find any key fragments to combine in your loot."


if __name__ == "__main__":
    CombineFragmentKeys().start()
