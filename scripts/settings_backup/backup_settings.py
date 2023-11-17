from __future__ import annotations

import json
from pathlib import Path

from common import AluConnector


class BackupSettings(AluConnector):
    """Backup League Settings to a json file.

    *Sometimes* League Client can behave really badly and occasionally it might result in a total wipe out of your settings.
    It happened to me during my casual playing session so IDK, the need of backup/restore functionality arose.

    This script saves your settings to `.temp/backup` folder:
    * game-settings.json
    * input-settings.json

    Which you can restore back with the "Restore Settings from Json" script.

    Note that this script will overwrite current json files in `.temp/backup` folder.
    """

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
