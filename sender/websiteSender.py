import click
import json
import logging

logger = logging.getLogger(__name__)

class WebsiteSender :

    def send(self, weekPrediction):
        logger.debug("je vais faire du html")