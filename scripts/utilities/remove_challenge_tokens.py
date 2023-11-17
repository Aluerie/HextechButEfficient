from __future__ import annotations

from common import AluConnector


class RemoveChallengeTokens(AluConnector):
    """Remove Challenge Tokens.

    Challenges are Evil. For some reason in Customize Identity tab you cannot reset your profile state.

    This script does exactly that: reset your challenge tokens to 3 empty slots.
    """

    async def callback(self) -> str:
        r = await self.post("/lol-challenges/v1/update-player-preferences/", data={"challengeIds": []})
        if r.status == 204:
            return f"Successfully removed challenge tokens"
        else:
            return f"Failed to remove challenges tokens with {r.status} status"


if __name__ == "__main__":
    RemoveChallengeTokens().start()
