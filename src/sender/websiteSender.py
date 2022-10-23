import logging
from datetime import datetime
from jinja2 import Environment, FileSystemLoader
import json

logger = logging.getLogger(__name__)

class WebsiteSender :

    def send(self, weekPrediction):
        self.generateFlyableDays(weekPrediction)
        self.generateAllDays(weekPrediction)
        #self.generateSpots()
    
    def generateFlyableDays(self, weekPrediction):
        logger.debug("Start generating markdown for flyableDays")
        print(json.dumps(weekPrediction,indent=4))
        #retire les jours pas flyable du tout
        flyablesDay = {}
        for date in weekPrediction:
            for spot, hours in weekPrediction[date].items():
                flyableHours = list(filter(lambda x: x.get('flyable') == True, hours))
                if len(flyableHours) == 0:
                    continue
                if flyablesDay.get(date,None) is None and len(flyableHours) > 0:
                    flyablesDay[date] = {}
                if flyablesDay.get(date,None) is not None and flyablesDay[date].get(spot,None) is None and len(flyableHours) > 0:
                    flyablesDay[date][spot] = []
                if len(flyableHours) > 0:
                    flyablesDay[date][spot] = flyablesDay[date][spot] + hours
        print(json.dumps(flyablesDay,indent=4))
        sortedPrediction = {}
        for date in sorted(flyablesDay.keys()):
            sortedPrediction[datetime.fromtimestamp(int(date)).strftime('%A %d %B')] = flyablesDay[date]        

        print(json.dumps(sortedPrediction, indent=4))
        file_loader = FileSystemLoader('src/templates')
        env = Environment(loader=file_loader)
        template = env.get_template('index.j2')
        template.globals['now'] = datetime.now().strftime('%A %d %B %H:%M')
        output = template.render(weekPrediction=sortedPrediction)

        f = open("index.markdown","w")
        f.write(output)
        f.close()
        logger.debug("Markdown generated")

    def generateAllDays(self, weekPrediction):
        logger.debug("Start generating markdown for allDays")
       #retire les jours pas flyable 
        sortedPrediction = {}
        for date in sorted(weekPrediction.keys()):
            sortedPrediction[datetime.fromtimestamp(int(date)).strftime('%A %d %B')] = weekPrediction[date]        

        file_loader = FileSystemLoader('src/templates')
        env = Environment(loader=file_loader)
        template = env.get_template('all.j2')
        template.globals['now'] = datetime.now().strftime('%A %d %B %H:%M')
        output = template.render(weekPrediction=sortedPrediction)

        f = open("all.markdown","w")
        f.write(output)
        f.close()
        logger.debug("Markdown generated")

    def generateSpots(self, spots):
        file_loader = FileSystemLoader('src/templates')
        env = Environment(loader=file_loader)
        template = env.get_template('spots.j2')
        template.globals['now'] = datetime.now().strftime('%A %d %B %H:%M')
        output = template.render(spots=spots)

        f = open("sites.markdown","w")
        f.write(output)
        f.close()
        logger.debug("Markdown generated")