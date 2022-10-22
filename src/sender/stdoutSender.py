import json
from datetime import datetime
import logging 

logger = logging.getLogger(__name__)

class StdoutSender :

    def send(self, weekPrediction):
        logger.debug("stdout sender in progress")
        prettyWeek = {}
        for key in weekPrediction:
            prettyWeek[datetime.fromtimestamp(int(key)).strftime('%A %d %B')] =  weekPrediction[key]
        logger.debug(json.dumps(prettyWeek, indent=4))