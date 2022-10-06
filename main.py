#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import locale
import json
import click
import logging
from parser.windyParser import WindyParser
from util.logger import getLogger

locale.setlocale(locale.LC_TIME, "fr_FR")
logger = getLogger("paragliding-forecast", False)

def getConfig(config_file):
    f = open(config_file)
    config = json.loads(f.read())
    sender = config["sender"]
    groupId = config["groupID"]
    f.close()
    return sender, groupId

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

def sendSignalMessage(message, sender, group_id):
   result = requests.post('http://localhost:8080/v2/send',headers={"Content-Type":"application/json"}, json={"message": message , "number": sender, "recipients": [group_id]})
   logger.debug(f"Signal status_code : {result.status_code}")
   logger.debug(f"Signal response : {result.text}")
 
def pushResultsOnSignal(result, sender, group_id):
    logger.debug(f"Send results to Signal")
    sendSignalMessage(f"Analyse du {datetime.now().strftime('%A %d %B %H:%M')}", sender, group_id)
    for date in sorted(result.keys()):
        message = f"\n## {datetime.fromtimestamp(int(date)).strftime('%A %d %B')} ## \n\n"
        for spot,hours in result[date].items():
            message += f"*****{spot.upper()}***** \n"
            for hour in hours:
                message += f"\t - {hour['hour']} -> {hour['meanWind']}-{hour['maxWind']}km/h, {hour['direction']}, Pluie : {hour['precipitation']} \n"
            message += "\n\n"
        sendSignalMessage(message, sender, group_id)
    if len(result.items()) == 0:
        sendSignalMessage("Ca ne vole nul part, profites en pour apprendre a plier ton parachute de secours", sender, group_id)


@click.command()
@click.option("--spot-file", required=True, type=str)
@click.option("--config-file", required=True, type=str)
@click.option("--send-to-signal", is_flag=True)
@click.option("--verbose", "-v", is_flag=True, help="Be verbose please")
def processWeather(spot_file, config_file, verbose, send_to_signal):
    logger.setLevel(logging.DEBUG if verbose else logging.INFO)
    logger.debug(f"Parameters :  spot_file : {spot_file}, config_file: {config_file}")
    spots = getSpots(spot_file)
    sender, group_id = getConfig(config_file)
    result = scrapeSpots(spots)
    result = getResultsByDay(result)
    logger.debug(json.dumps(result, indent=4))
    if send_to_signal:
        pushResultsOnSignal(result, sender, group_id)

if __name__ == "__main__":
    processWeather()