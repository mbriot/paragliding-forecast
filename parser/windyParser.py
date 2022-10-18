from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from util.directions import windDirections 
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
        try:
            WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'td-days')))
        except TimeoutException:
            raise("Loading took too much time!")

        self.driver.find_element(By.XPATH, "//div[@id='detail-box']/div[2]/div[1]").click() # click on Basic
        self.driver.find_element(By.XPATH, "//div[@id='detail-box']/div[3]/div[8]").click() # click on Arome
        time.sleep(3)
        htmlElements = self.driver.page_source
        self.driver.close()
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
            if int(hour) < 8 or int(hour) > 17:
                continue
            hour = str(hour) + "h-" + str(int(hour) + 3) + "h"
            timestamp = hours[i].get('data-ts')
            direction = windDirections[int(re.search('[0-9]+', directions[i].div.get('style')).group())]
            maxWind = maxWinds[i].get_text()
            meanWind = meanWinds[i].get_text()
            precipitation = precipitations[i].get_text()
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
                if len(dayResult["slots"]) > 0 :
                    spotResult["dates"].append(dayResult)
                dayResult = { "day": asTimestamp, "slots": [] }

            if direction in self.goodDirections and int(meanWind) >= self.minSpeed and int(maxWind) <= self.maxSpeed and int(float(precipitation or 0)) <= 3 :
                dayResult["slots"].append({"hour" : hour, "meanWind": meanWind, "maxWind": maxWind, "direction": direction, "precipitation": precipitation, "balise": self.balise, "url": self.spotUrl })
        
        logger.info(f"End parsing html for spot {self.spotName}") 
        return spotResult 
    
    def getLastModelUpdate(self, html):
        logger.debug("start checking last windy model update")
        soup = BeautifulSoup(html,"html.parser")
        result = soup.find("span", { "class" : "dbitem model-info mobilehide" }).get_text()
        logger.debug(f"windy saying last update model was {result}")
        result = result.replace(chr(160),chr(32))
        logger.debug(f"windy after replace strange chars saying last update model was {result}")
        hourToRemove = 0
        if re.search('([0-9]+) h', result) is not None:
            hourToRemove = int(re.search('([0-9]+) h',result).group(1))
        if re.search('([0-9]+)h', result) is not None:
            hourToRemove = int(re.search('([0-9]+)h',result).group(1))
        logger.debug(f"remove {hourToRemove} hours to {datetime.now().strftime('%A %d %B %H')}")
        lastUpdate = (datetime.now() - timedelta(hours=hourToRemove)).strftime('%A %d %B %H') 
        logger.debug("end checking last windy model update")
        return lastUpdate

