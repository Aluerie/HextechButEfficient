import json

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
            f = open(f"settings/.backup/{item}.json")
            data = json.load(f)
            req = await connection.request("patch", f"/lol-game-settings/v1/{item}", data=data)
            print(f"{item} req status: {req.status}")


@connector.close
async def disconnect(_):
    print("The client have been closed!")


connector.start()
