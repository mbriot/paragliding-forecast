import click
import json
from util.logger import getLogger
import requests
import datetime

class StdoutSender :

    def __init__(self):
        self.stdoutLogger = getLogger("stdoutSender", click.get_current_context().params['verbose'])
    
    def send(self, weekPrediction):
        print("stdout sender in progress")
        self.stdoutLogger.debug(json.dumps(weekPrediction, indent=4))