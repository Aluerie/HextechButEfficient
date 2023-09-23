from lcu_driver import Connector

connector = Connector()


@connector.ready
async def connect(connection):
    print("LCU API is ready to be used.")
    summoner = await connection.request("get", "/lol-summoner/v1/current-summoner")
    if summoner.status != 200:
        print("Please login into your account and restart the script...")
    else:
        req = await connection.request(
            "post", "/lol-challenges/v1/update-player-preferences/", data={"challengeIds": []}
        )
        print(f"Req status: {req.status}")


@connector.close
async def disconnect(_):
    print("The client have been closed!")


connector.start()
