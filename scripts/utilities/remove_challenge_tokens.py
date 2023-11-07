from __future__ import annotations

from common import AluConnector


class RemoveChallengeTokens(AluConnector):
    async def callback(self) -> str:
        r = await self.post("/lol-challenges/v1/update-player-preferences/", data={"challengeIds": []})
        if r.status == 204:
            return f"Successfully removed challenge tokens"
        else:
            return f"Failed to remove challenges tokens with {r.status} status"


if __name__ == "__main__":
    RemoveChallengeTokens().start()
