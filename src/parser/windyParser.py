from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from util.directions import windDirections, neighbourgDirections
import re
from datetime import datetime, timedelta
import time
from bs4 import BeautifulSoup
import locale
locale.setlocale(locale.LC_TIME, "fr_FR")
import logging

logger = logging.getLogger(__name__)
seleniumLogger = logging.getLogger('selenium.webdriver.remote.remote_connection')
seleniumLogger.setLevel(logging.WARNING)
ulrlib3Logger = logging.getLogger('urllib3.connectionpool')
ulrlib3Logger.setLevel(logging.WARNING)

class WindyParser :

    kmhToNode = 1.852

    def __init__(self, spot):
        self.spotName = spot["name"]
        self.spotUrl = spot["url"]
        self.minSpeed = spot["minSpeed"]
        self.maxSpeed = spot["maxSpeed"]
        self.goodDirections = spot["goodDirection"]
        self.excludeDays = spot.get("excludeDays", None)
        self.monthsToExclude = spot.get("monthsToExcludes",None)
        self.balise = spot.get("balise",None)
        options = FirefoxOptions()
        options.add_argument("--headless")
        self.driver = webdriver.Firefox(options=options)

    def getHtml(self):
        logger.debug(f"start processing spot {self.spotName}")
        self.driver.get(f"https://www.windy.com/{self.spotUrl}")
        logger.debug(f"Page loaded for spot {self.spotName}")
        try:
            logger.debug(f"Wait for data to arrive in prediction table for spot {self.spotName}")
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'td-days')))
            logger.debug(f"data well arrived for spot {self.spotName}")
        except TimeoutException:
            logger.debug(f"Timeout waiting for prediction table for spot {self.spotName}")
            raise Exception("Loading took too much time!")

        self.driver.find_element(By.XPATH, "//div[@id='detail-box']/div[2]/div[1]").click() # click on Basic
        self.driver.find_element(By.XPATH, "//div[@id='detail-box']/div[3]/div[8]").click() # click on Arome
        time.sleep(3)
        htmlElements = self.driver.page_source
        self.driver.quit()
        return htmlElements
    
    def processHtml(self, html):
        logger.info(f"Start parsing html for spot {self.spotName}")
        soup = BeautifulSoup(html,"html.parser")
        result = soup.find("table", { "id" : "detail-data-table" })

        rows = result.findAll("tr")
        hours = rows[1].findAll("td")
        directions = rows[7].findAll("td")
        meanWinds = rows[5].findAll("td")
        maxWinds = rows[6].findAll("td")
        precipitations = rows[4].findAll("td")

        spotResult = {
            "name": self.spotName,
            "url": self.spotUrl,
            "balise": self.balise,
            "dates": []
        }
        now = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0).timestamp()
        dayResult = { "day": now, "slots": [] }
        for i in range(len(hours)):
            hour = hours[i].get_text()
            if int(hour) < 7 or int(hour) > 17:
                continue
            hour = str(hour) + "h-" + str(int(hour) + 3) + "h"
            timestamp = hours[i].get('data-ts')
            direction = windDirections[int(re.search('[0-9]+', directions[i].div.get('style')).group())]
            maxWind = maxWinds[i].get_text()
            meanWind = meanWinds[i].get_text()
            precipitation = precipitations[i].get_text().replace("cm","").replace("mm","")
            datetimeDay = datetime.fromtimestamp(int(timestamp[:-3])).replace(hour=0, minute=0, second=0, microsecond=0)
            
            # don't process slot if in a not flyable day due to rules
            if self.excludeDays and self.monthsToExclude :
                if datetimeDay.month in self.monthsToExclude and datetimeDay.weekday() in self.excludeDays:
                    continue

            logger.debug(f"{datetimeDay.strftime('%A %d %B')}:{hour} -> {meanWind}-{maxWind}kt {direction} ,pluie : {precipitation}")
            maxWind = str(int(float(maxWind) * self.kmhToNode))
            meanWind = str(int(float(meanWind) * self.kmhToNode))
            asTimestamp = datetimeDay.timestamp()
            if asTimestamp != now:
                now = asTimestamp
                if len(dayResult['slots']) != 0 :
                    dayResult = self.setScore(dayResult)
                    spotResult["dates"].append(dayResult)
                dayResult = { "day": asTimestamp, "slots": [] }
            slot = {"hour" : hour, "meanWind": meanWind, "maxWind": maxWind, "direction": direction, "precipitation": precipitation, "balise": self.balise, "url": self.spotUrl, "goodDirection": ", ".join(self.goodDirections), "minSpeed": self.minSpeed, "maxSpeed": self.maxSpeed }
            slot['flyable'] = True if direction in self.goodDirections and int(meanWind) >= self.minSpeed and int(maxWind) <= self.maxSpeed and int(float(precipitation or 0)) <= 3  else False
            dayResult["slots"].append(slot)
        
        # Don't show if I only have the beginning of the last day
        if len(dayResult['slots']) == 4 :
            dayResult = self.setScore(dayResult)
            spotResult["dates"].append(dayResult)
        logger.info(f"End parsing html for spot {self.spotName}") 

        return spotResult 

    def setScore(self, dayResult):
        score = 0
        i = 0
        for slot in dayResult['slots']:
            logger.debug(f"[SCORING] set score for slot {str(i)}")
            scoreBefore = score
            if slot['flyable']:
                logger.debug(f"[SCORING] slot is flyable, give 1000 points")
                score += 1000
                continue

            # DIRECTION
            if slot['direction'] in slot['goodDirection'].split(','):
                logger.debug(f"[SCORING] slot in good direction, give 200 points")
                score += 200
            # direction presque bonne 25
            neighbourgDirection = neighbourgDirections[slot['direction']]
            if slot['direction'] not in slot['goodDirection'].split(',') and any(x in slot['goodDirection'].split(',') for x in neighbourgDirection):
                logger.debug(f"[SCORING] slot in almost good direction, give 100 points")
                score += 100

            # VENT
            # parfait = 25
            if int(slot['meanWind']) >= slot['minSpeed'] and int(slot['maxWind']) <= slot['maxSpeed']:
                logger.debug(f"[SCORING] wind is perfect, give 25 points")
                score += 25
            # leger au dessus : 15
            if int(slot['maxWind']) >= slot['maxSpeed'] and int(slot['maxWind']) <= slot['maxSpeed'] + 10:
                logger.debug(f"[SCORING] wind is a little bit stronger, give 15 points")
                score += 15
            # trop bas mais pas trop haut : 15
            if int(slot['meanWind']) <= slot['minSpeed'] and int(slot['maxWind']) <= slot['maxSpeed']:
                logger.debug(f"[SCORING] wind too slow, give 25 points")
                score += 15
            # bcoup trop au dessus 5
            if int(slot['maxWind']) >= slot['maxSpeed'] and int(slot['maxWind']) >= slot['maxSpeed'] + 10:
                logger.debug(f"[SCORING] wind way too strong, give 5 points")
                score += 5
            
            # PLUIE
            precipitation = 0.0 if slot['precipitation'] == "" else float(slot['precipitation'].replace("cm","").replace("mm",""))
            # pas de pluie 10
            if precipitation == 0.0:
                logger.debug(f"[SCORING] no precipitation, give 10 points")
                score += 10
            # moins de 1 : 5
            if precipitation < 1.0:
                logger.debug(f"[SCORING] precipitation under 1.0, give 5 points")
                score += 5
            logger.debug(f"slot {str(i)} got a score of {str(score - scoreBefore)}")
            i += 1

        logger.debug(f"slots got a score of {str(score)}")
        dayResult['slots'][0]['score'] = score
        return dayResult
