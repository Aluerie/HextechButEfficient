from __future__ import annotations

from typing import Mapping, NamedTuple

from common import AluConnector, TabularData


class ShardToDisenchant(NamedTuple):
    type: str
    loot_id: str
    count: int
    display_name: str
    disenchant_value: int
    

class BEMassDisenchantEverything(AluConnector):
    """Blue Essence Mass Disenchant everything.
    
    This script disenchants every possible champion shard, including permanents.
    Only use this if you don't care about saving shards for champion mastery upgrades or unlocking champions.
    
    The script will show the list of shards to disenchant and then you will be able to confirm/deny the procedure."""
    
    async def callback(self: AluConnector) -> str:
        # Loot
        r_loot = await self.get("/lol-loot/v1/player-loot")
        
        # Gather statistics of the shards to disenchant :>
        shards_to_confirm: list[ShardToDisenchant] = []
        for item in await r_loot.json():
            extra_display_text = ""
            match item["type"]:
                case "CHAMPION": # permanent champion shard
                    extra_display_text = " Permanent"
                case _:
                    continue
            
            shards_to_disenchant = max(0, item["count"])
            
            if shards_to_disenchant:
                shards_to_confirm.append(
                    ShardToDisenchant(
                        type=item["type"],
                        loot_id=item["lootId"],
                        count=shards_to_disenchant,
                        display_name=item["itemDesc"] + extra_display_text,
                        disenchant_value=item["disenchantValue"]
                    )
                )
        
        # Confirm
        if not shards_to_confirm:
            text = "No shards to disnechant."
            self.output(text)
        else:
            text = "The following Champion shards will be disenchanted:\n"
            table = TabularData()
            table.set_columns(["Shard Name", "Amount", "BE Value"])
            rows = [(shard.display_name, shard.count, shard.disenchant_value) for shard in shards_to_confirm]
            table.add_rows(rows)
            text += table.render()
            total_be = sum(shard.disenchant_value * shard.count for shard in shards_to_confirm)
            text += f"\nTotal Amount of Blue Essence to gain: {total_be}"
            
            self.confirm(text)
        
        # Disenchant every possible shard
        total_shards_disenchanted = 0
        for shard in shards_to_confirm:
            r = await self.post(
                f"/lol-loot/v1/recipes/{shard.type}_disenchant/craft?repeat={shard.count}",
                data=[shard.loot_id],
            )
            if r.ok:
                total_shards_disenchanted += shard.count
        
        return f"Disenchanted {total_shards_disenchanted} shards"


if __name__ == "__main__":
    BEMassDisenchantEverything().start()