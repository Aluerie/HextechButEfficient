import json
from pathlib import Path

from lcu_driver import Connector

connector = Connector()


@connector.ready
async def connect(connection):
    print("LCU API is ready to be used.")
    summoner = await connection.request("get", "/lol-summoner/v1/current-summoner")
    if summoner.status != 200:
        print("Please login into your account and restart the script...")
    else:
        for item in ["game-settings", "input-settings"]:
            req = await connection.request("get", f"/lol-game-settings/v1/{item}")
            data = await req.json()
            # pprint.pprint(gs_json)

            # ensure .temp folder
            backup_dir = "settings/.backup/"
            Path(backup_dir).mkdir(parents=True, exist_ok=True)
            with open(f"{backup_dir}{item}.json", "w") as f:
                json.dump(data, f, indent=4)
            print(f"{item} req status: {req.status}")


@connector.close
async def disconnect(_):
    print("The client have been closed!")


connector.start()
