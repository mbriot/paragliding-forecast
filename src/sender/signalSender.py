import click
import json
import requests
from datetime import datetime
import logging 
from util.util import getDaysWithOnlyFlyablesSlots

logger = logging.getLogger(__name__)

class SignalSender :

    def __init__(self):
        self.configPath = click.get_current_context().params['config_file']
    
    def send(self, weekPrediction):
        f = open(self.configPath)
        config = json.loads(f.read())
        self.sender = config["sender"]
        self.groupId = config["groupID"]
        f.close()

        flyablesDay = getDaysWithOnlyFlyablesSlots(weekPrediction)
    
        logger.debug(f"Send results to Signal")
        if len(flyablesDay.items()) == 0:
            logger.info("It does not fly anywhere anytime soon, nothing to send")
            return
        self.sendSignalMessage(f"Analyse du {datetime.now().strftime('%A %d %B %H:%M')}")
        self.sendSignalMessage(f"Résultats en détail sur https://parapente-dans-le-nord.github.io")
        for date in sorted(flyablesDay.keys()):
            message = f"\n## {datetime.fromtimestamp(int(date)).strftime('%A %d %B')} ## \n\n"
            for spot,hours in flyablesDay[date].items():
                message += f"*****{spot.upper()}***** \n"
                for hour in hours:
                    if hour["precipitation"] == "":
                        precipitation = "0mm/h 🌞"
                    else :
                        precipitation = hour["precipitation"] + "mm/h 🌧️"
                    message += f"\t - {hour['hour']} -> {hour['meanWind']}-{hour['maxWind']}km/h, {hour['direction']}, Pluie : {precipitation} \n"
                message += "\n\n"
            self.sendSignalMessage(message)

    def sendSignalMessage(self, message):
        result = requests.post('http://localhost:8080/v2/send',headers={"Content-Type":"application/json"}, json={"message": message , "number": self.sender, "recipients": [self.groupId]})
        logger.debug(f"Signal status_code : {result.status_code}, response {result.text}")