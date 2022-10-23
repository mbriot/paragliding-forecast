import click
import json
import requests
from datetime import datetime
import logging 

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

        logger.debug(f"Send results to Signal")
        if len(weekPrediction.items()) == 0:
            return
        self.sendSignalMessage(f"Analyse du {datetime.now().strftime('%A %d %B %H:%M')}")
        for date in sorted(weekPrediction.keys()):
            message = f"\n## {datetime.fromtimestamp(int(date)).strftime('%A %d %B')} ## \n\n"
            for spot,hours in weekPrediction[date].items():
                onlyFlyableHours = list(filter(lambda x: x.get('flyable') == True, hours))
                message += f"*****{spot.upper()}***** \n"
                for hour in onlyFlyableHours:
                    message += f"\t - {hour['hour']} -> {hour['meanWind']}-{hour['maxWind']}km/h, {hour['direction']}, Pluie : {hour['precipitation']} \n"
                message += "\n\n"
            self.sendSignalMessage(message)

    def sendSignalMessage(self, message):
        result = requests.post('http://localhost:8080/v2/send',headers={"Content-Type":"application/json"}, json={"message": message , "number": self.sender, "recipients": [self.groupId]})
        logger.debug(f"Signal status_code : {result.status_code}, response {result.text}")