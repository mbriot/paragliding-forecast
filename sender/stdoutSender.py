import click
import json
from util.logger import getLogger
from datetime import datetime

class StdoutSender :

    def __init__(self):
        self.stdoutLogger = getLogger("stdoutSender", click.get_current_context().params['verbose'])
    
    def send(self, weekPrediction):
        print("stdout sender in progress")
        prettyWeek = {}
        for key in weekPrediction:
            prettyWeek[datetime.fromtimestamp(int(key)).strftime('%A %d %B')] =  weekPrediction[key]
        self.stdoutLogger.debug(json.dumps(prettyWeek, indent=4))