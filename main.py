#!/usr/bin/env python3
import locale
import json
import click
import os
from parser.windyParser import WindyParser
from sender.sender import PredictionSender
import logging
from datetime import datetime

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
        windyParser = WindyParser(spot)
        html = windyParser.getHtml()
        spotResult = windyParser.processHtml(html)
        result.append(spotResult)
    return result

def getResultsByDay(result):
    resultByDay = {}
    for spotResult in result:
        spotName = spotResult["name"]
        for date in spotResult["dates"]:
            if resultByDay.get(date["day"],None) is None:
                resultByDay[date["day"]] = {}
            for slot in date["slots"]:
                slot["name"] = spotName
                if resultByDay[date["day"]].get(spotName,None) is None:
                    resultByDay[date["day"]][spotName] = []
                resultByDay[date["day"]][spotName].append(slot)
    
    return resultByDay

def needToProcess(spot):
    windyParser = WindyParser(spot)
    html = windyParser.getHtml()
    lastWindyUpdate = windyParser.getLastModelUpdate(html)
    logger.debug(f"found lastWindyUpdate to be {lastWindyUpdate}")
    if os.path.isfile(lastAromeFile) is False:
        f = open(lastAromeFile,"w"); f.close()
    f = open(lastAromeFile,"r")
    lastUpdate = f.read()
    logger.debug(f"found last process date to be {lastUpdate}")
    f.close()
    if lastUpdate == "" or lastUpdate != lastWindyUpdate:
        return (True, lastWindyUpdate)
    else:
        return (False, lastWindyUpdate)

@click.command()
@click.option("--spot-file", required=True, type=str)
@click.option("--config-file", required=True, type=str)
@click.option("--send-to-signal", is_flag=True)
@click.option("--send-to-website", is_flag=True)
@click.option("--send-to-stdout", is_flag=True)
@click.option("--verbose", "-v", is_flag=True, help="Be verbose please")
@click.option("--process-anyway", is_flag=True)
def processWeather(spot_file, config_file, verbose, send_to_signal, send_to_website, send_to_stdout, process_anyway):
    logger.setLevel(logging.DEBUG if verbose else logging.INFO)
    logger.debug(f"Parameters :  spot_file : {spot_file}, config_file: {config_file}")
    spots = getSpots(spot_file)
    if process_anyway is False:
        need, lastAromeUpdate = needToProcess(spots[0])
        if need is False:
            logger.info("prevision déjà a jour, pas besoin d'aller plus loin")
            exit(0)

    try:
        predictions = scrapeSpots(spots)
    except Exception as e:
        logger.error("There was an error scraping spots")
        logger.debug(e)
        exit(1)
    predictions = getResultsByDay(predictions)
    lastAromeUpdate = datetime.now().strftime('%A %d %B %H:%M') if process_anyway is True else lastAromeUpdate
    PredictionSender().send(predictions,lastAromeUpdate)
    f = open(lastAromeFile,"w")
    f.write(lastAromeUpdate)
    f.close()
    

if __name__ == "__main__":
    processWeather()