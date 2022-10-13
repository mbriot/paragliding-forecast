import click
import json
from util.logger import getLogger
import requests
import datetime

class WebsiteSender :

    def __init__(self):
        self.websiteLogger = getLogger("websiteSender", click.get_current_context().params['verbose'])
    
    def send(self, weekPrediction):
        print("je vais faire du html")