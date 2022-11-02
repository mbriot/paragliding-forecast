#!/usr/bin/env python3
import locale
import json
import click
from parser.windyParser import WindyParser
from sender.sender import PredictionSender
import logging
import traceback
from util.util import getResultByDay

logger = logging.getLogger()
ch = logging.StreamHandler()
ch.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
logger.addHandler(ch)

locale.setlocale(locale.LC_TIME, "fr_FR")

lastAromeFile = "/tmp/lastAromeUpdate"

def getSpots(spot_file):
    f = open(spot_file)
    spots = json.loads(f.read())["spots"]
    f.close()
    return spots

def scrapeSpots(spots) :
    result = []
    for spot in spots:
        for retryNumber in range(3):
            try:
                windyParser = WindyParser(spot)
                html = windyParser.getHtml()
                spotResult = windyParser.processHtml(html)
                result.append(spotResult)
                break
            except Exception as e:
                logger.info(f"exception number {retryNumber} while parsing spot {spot['name']}")
                traceback.print_exc()
                continue
    return result

@click.command()
@click.option("--spot-file", required=True, type=str)
@click.option("--config-file", required=False, type=str)
@click.option("--send-to-signal", is_flag=True)
@click.option("--send-to-website", is_flag=True)
@click.option("--send-to-stdout", is_flag=True)
@click.option("--verbose", "-v", is_flag=True, help="Be verbose please")
def processWeather(spot_file, config_file, verbose, send_to_signal, send_to_website, send_to_stdout):
    logger.setLevel(logging.DEBUG if verbose else logging.INFO)
    logger.debug(f"Parameters :  spot_file : {spot_file}, config_file: {config_file}")
    spots = getSpots(spot_file)
    try:
        predictions = scrapeSpots(spots)
    except Exception:
        logger.error("There was an error scraping spots")
        traceback.print_exc()
        exit(1)

    predictions = getResultByDay(predictions)
    PredictionSender().send(predictions)

if __name__ == "__main__":
    processWeather()
