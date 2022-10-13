import click
import json
from util.logger import getLogger
import requests
from datetime import datetime

class SignalSender :

    def __init__(self):
        self.configPath = click.get_current_context().params['config_file']
        self.predictionLogger = getLogger("signalSender", click.get_current_context().params['verbose'])
    
    def send(self, weekPrediction):
        f = open(self.configPath)
        config = json.loads(f.read())
        self.sender = config["sender"]
        self.groupId = config["groupID"]
        f.close()

        self.predictionLogger.debug(f"Send results to Signal")
        self.sendSignalMessage(f"Analyse du {datetime.now().strftime('%A %d %B %H:%M')}")
        for date in sorted(weekPrediction.keys()):
            message = f"\n## {datetime.fromtimestamp(int(date)).strftime('%A %d %B')} ## \n\n"
            for spot,hours in weekPrediction[date].items():
                message += f"*****{spot.upper()}***** \n"
                for hour in hours:
                    message += f"\t - {hour['hour']} -> {hour['meanWind']}-{hour['maxWind']}km/h, {hour['direction']}, Pluie : {hour['precipitation']} \n"
                message += "\n\n"
            self.sendSignalMessage(message)
        if len(weekPrediction.items()) == 0:
            self.sendSignalMessage("Ca ne vole nul part, profites en pour apprendre a plier ton parachute de secours")

    def sendSignalMessage(self, message):
        result = requests.post('http://localhost:8080/v2/send',headers={"Content-Type":"application/json"}, json={"message": message , "number": self.sender, "recipients": [self.groupId]})
        self.predictionLogger.debug(f"Signal status_code : {result.status_code}, response {result.text}")