#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import locale
import json

locale.setlocale(locale.LC_TIME, "fr_FR")

f = open('config.json')
config = json.loads(f.read())
sender = config["sender"]
groupId = config["groupID"]
f.close()

def getSpots():
    f = open('spots.json')
    return json.loads(f.read())["spots"]

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

        current_date = datetime.now()
        for day in range(1,8): 
            resp = requests.get(f'https://www.meteoblue.com/fr/meteo/semaine/{technicalSpotName}?day={day}')
            soup = BeautifulSoup(resp.content, features="html.parser")
            current_date = current_date if day == 1 else current_date + timedelta(days=1)
            dayResult = {
                "day": current_date.strftime("%A %d %B"),
                "slots": []
            }
            trs = soup.find_all('tr')
            for tr in trs:
                if tr.get("title") == 'Vitesse du vent (km/h)':
                    wind_speeds = tr.get_text().split('\n')
                    wind_speeds = list(filter(None, wind_speeds))
                    for i in [("9h-12h",7,8),("12h-15h",10,11),("15h-18h",13,14)]:
                        actualMinSpeed = int(wind_speeds[i[2]].strip().split('-')[0])
                        actualMaxSpeed = int(wind_speeds[i[2]].strip().split('-')[1])
                        actualDirection = wind_speeds[i[1]].strip()
                        if actualDirection in goodDirection and actualMinSpeed >= minSpeed and actualMaxSpeed <= maxSpeed :
                            dayResult["slots"].append({"hour" : i[0], "speed": wind_speeds[i[2]].strip(), "direction": actualDirection})
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

def pushResultsOnSignal(result):
    message = ""
    for date,spot in result.items():
        message += f"\n##### {date} ##### \n"
        for spot,hours in spot.items():
            message += f"*****{spot.upper()}***** \n"
            for hour in hours:
                message += f"\t - {hour['hour']} -> {hour['speed']}km/h, {hour['direction']} \n"
    result = requests.post('http://localhost:8080/v2/send',headers={"Content-Type":"application/json"}, json={"message": message , "number": sender, "recipients": [groupId]})

if __name__ == "__main__":
    spots = getSpots()
    result = scrapeSpots(spots)
    result = getResultsByDay(result)
    pushResultsOnSignal(result)
    