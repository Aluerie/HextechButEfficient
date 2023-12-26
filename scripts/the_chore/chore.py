from __future__ import annotations

import logging

from common import AluConnector
from scripts.be_management import BEMassDisenchant, BEMassOpening
from scripts.utilities import CombineFragmentKeys

log = logging.getLogger(__name__)


class TheChore(AluConnector):
    """
    This gathers all chores that I personally would love to do in just one click.
    """

    async def callback(self) -> str:
        script_list = (
            BEMassOpening,
            BEMassDisenchant,
            CombineFragmentKeys,
        )
        for cls in script_list:
            script_result = await cls.callback(self)  # type: ignore # idk bro
            log.info(script_result)

        return "Chore is finished"


if __name__ == "__main__":
    TheChore().start()
