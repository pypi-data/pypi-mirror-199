# stackd instance


from stackdiac.api import app as api_app
from .stackd import Stackd
sd = Stackd()

@api_app.get("/sd")
async def get_sd() -> Stackd:
    return sd

import logging

logger = logging.getLogger(__name__)

