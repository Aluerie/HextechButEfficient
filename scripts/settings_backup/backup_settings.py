from __future__ import annotations

import json
from pathlib import Path

from common import AluConnector


class BackupSettings(AluConnector):
    async def callback(self) -> str:
        result: list[str] = []
        for item in ["game-settings", "input-settings"]:
            r = await self.get(f"/lol-game-settings/v1/{item}")
            data = await r.json()
            # pprint.pprint(gs_json)

            # ensure .temp folder
            backup_dir = ".temp/backup"
            Path(backup_dir).mkdir(parents=True, exist_ok=True)
            with open(f"{backup_dir}/{item}.json", "w") as file:
                json.dump(data, file, indent=4)
            result.append(f"{item} req status: {r.status}.")
        return " ".join(result)


if __name__ == "__main__":
    BackupSettings().start()
