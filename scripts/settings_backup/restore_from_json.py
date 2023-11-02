from __future__ import annotations

import json

from common import AluConnector


class RestoreSettings(AluConnector):
    async def callback(self) -> str:
        result: list[str] = []
        for item in ["game-settings", "input-settings"]:
            with open(f"scripts/settings_backup/.backup/{item}.json") as file:
                data = json.load(file)
            r = await self.patch(f"/lol-game-settings/v1/{item}", data=data)
            result.append(f"{item} req status: {r.status}.")
        return " ".join(result)


if __name__ == "__main__":
    RestoreSettings().start()
