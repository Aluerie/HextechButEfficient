from __future__ import annotations

from common import AluConnector


class RemoveChallengeTokens(AluConnector):
    async def callback(self) -> str:
        r = await self.post("/lol-challenges/v1/update-player-preferences/", data={"challengeIds": []})
        if r.status == 204:
            result = f"Successfully removed challenge tokens"
        else:
            result = f"Failed to remove challenges tokens with {r.status} status"
        return result
        


def remove_challenge_tokens():
    connector = RemoveChallengeTokens()
    connector.start()
    return connector.result


if __name__ == "__main__":
    remove_challenge_tokens()
