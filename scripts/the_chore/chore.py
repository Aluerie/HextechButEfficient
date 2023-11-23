from __future__ import annotations

from common import AluConnector
from scripts.be_management import BEMassDisenchant
from scripts.utilities import CombineFragmentKeys

import logging

log = logging.getLogger(__name__)


class TheChore(AluConnector):
    """
    This gathers all chores that I personally would love to do in just one click.
    """

    async def callback(self: AluConnector) -> str:
        r1 = await BEMassDisenchant.callback(self)
        log.info(r1)
        r2 = await CombineFragmentKeys.callback(self)
        log.info(r2)

        return "Chore is finished"


if __name__ == "__main__":
    TheChore().start()
