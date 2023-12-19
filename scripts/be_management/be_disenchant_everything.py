from __future__ import annotations

from .be_mass_disenchant import BaseBEDisenchant, ShardToDisenchant


class BEDisenchantEverything(BaseBEDisenchant):
    """Blue Essence Mass Disenchant everything.

    This script disenchants every possible champion shard, including permanents.
    Only use this if you don't care about saving shards for champion mastery upgrades or unlocking champions.

    The script will show the list of shards to disenchant and then you will be able to confirm/deny the procedure.
    """

    async def get_shards_to_confirm(self) -> list[ShardToDisenchant]:
        r_loot = await self.get("/lol-loot/v1/player-loot")

        # Gather statistics of the shards to disenchant :>
        shards_to_confirm: list[ShardToDisenchant] = []
        for item in await r_loot.json():
            match item["type"]:
                case "CHAMPION_RENTAL":
                    extra_display_text = ""
                case "CHAMPION":  # permanent champion shard
                    extra_display_text = " Permanent"
                case _:  # skip non-champion shard items
                    continue

            shards_to_disenchant = max(0, item["count"])

            if shards_to_disenchant:
                shards_to_confirm.append(
                    ShardToDisenchant(
                        type=item["type"],
                        loot_id=item["lootId"],
                        count=shards_to_disenchant,
                        display_name=item["itemDesc"] + extra_display_text,
                        disenchant_value=item["disenchantValue"],
                    )
                )
        return shards_to_confirm


if __name__ == "__main__":
    BEDisenchantEverything().start()
