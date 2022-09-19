#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import locale
import json
import click
import logging

locale.setlocale(locale.LC_TIME, "fr_FR")
logger = logging.getLogger("paragliding-forecast")
ch = logging.StreamHandler()
ch.setFormatter(logging.Formatter("%(name)s - %(levelname)s - %(message)s"))
logger.addHandler(ch)

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
        spotName = spot["name"]
        technicalSpotName = spot["technicalSpotName"]
        goodDirection = spot["goodDirection"]
        minSpeed = spot["minSpeed"]
        maxSpeed = spot["maxSpeed"]
        spotResult = {
            "name" : spotName,
            "dates" : [

            ]
        }

        logger.debug(
            f"Processing spot {spotName}, technicalSpotName: {technicalSpotName}, goodDirection: {goodDirection}, minSpeed: {minSpeed}, maxSpeed: {maxSpeed}"
        )

        current_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        for day in range(1,8): 
            resp = requests.get(f'https://www.meteoblue.com/fr/meteo/semaine/{technicalSpotName}?day={day}')
            soup = BeautifulSoup(resp.content, features="html.parser")
            current_date = current_date.timestamp() if day == 1 else current_date + 86400
            dayResult = {
                "day": current_date,
                "slots": []
            }
            logger.debug(f"Processing day {day} with date {datetime.fromtimestamp(int(current_date)).strftime('%A %d %B')}")
            windElements = soup.find_all('tr',{'class','windspeeds'})
            winds = [element.strip() for element in list(filter(None,windElements[0].get_text().split('\n')))][1:]
            precipitationsElements = soup.find_all('tr',{'class','precips'})
            precips = [element.strip() for element in list(filter(None,precipitationsElements[0].get_text().split('\n')))][2:]

            for i in [("9h-12h",6,7),("12h-15h",9,10),("15h-18h",12,13)]:
                actualMinSpeed = int(winds[i[2]].strip().split('-')[0])
                actualMaxSpeed = int(winds[i[2]].strip().split('-')[1])
                actualDirection = winds[i[1]].strip()
                quantityPrecipitation = int(precips[i[1]].replace(" mm","").replace("-","0").replace("< 1","1"))
                probabilityPrecipitation = int(precips[i[2]].replace("%",""))
                if actualDirection in goodDirection and actualMinSpeed >= minSpeed and actualMaxSpeed <= maxSpeed and (quantityPrecipitation <= 2 or probabilityPrecipitation < 50)  :
                    dayResult["slots"].append({"hour" : i[0], "speed": winds[i[2]].strip(), "direction": actualDirection, "precipitation": precips[i[1]], "probabilityPrecipitation": precips[i[2]]})

            if len(dayResult["slots"]) > 0 :
                spotResult["dates"].append(dayResult)
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
                message += f"\t - {hour['hour']} -> {hour['speed']}km/h, {hour['direction']}, Pluie : {hour['precipitation']}/{hour['probabilityPrecipitation']} \n"
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
    
    