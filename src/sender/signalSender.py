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

        # Remove slots marked as flyable False to get only flyable days
        flyablesDay = {}
        for date in weekPrediction:
         for spot, hours in weekPrediction[date].items():
            flyableHours = list(filter(lambda x: x.get('flyable') == True, hours))
            if flyablesDay.get(date,None) is None and len(flyableHours) > 0:
                flyablesDay[date] = {}
            if flyablesDay.get(date,None) is not None and flyablesDay[date].get(spot,None) is None and len(flyableHours) > 0:
                flyablesDay[date][spot] = []
            if len(flyableHours) > 0:
                flyablesDay[date][spot] = flyablesDay[date][spot] + flyableHours
    
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
                    message += f"\t - {hour['hour']} -> {hour['meanWind']}-{hour['maxWind']}km/h, {hour['direction']}, Pluie : {hour['precipitation']} \n"
                message += "\n\n"
            self.sendSignalMessage(message)

    def sendSignalMessage(self, message):
        result = requests.post('http://localhost:8080/v2/send',headers={"Content-Type":"application/json"}, json={"message": message , "number": self.sender, "recipients": [self.groupId]})
        logger.debug(f"Signal status_code : {result.status_code}, response {result.text}")