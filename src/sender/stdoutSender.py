import json
from datetime import datetime
import logging 
from util.util import sortByDate

logger = logging.getLogger(__name__)

class StdoutSender :

    def send(self, weekPrediction):
        logger.debug("stdout sender in progress")
        sortedPrediction = sortByDate(weekPrediction)
        logger.debug(json.dumps(sortedPrediction, indent=4))