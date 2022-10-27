import logging
from datetime import datetime
from jinja2 import Environment, FileSystemLoader
from util.util import sortByDate, getDaysWithAtLeastOneSlot
import json 
import calendar 
logger = logging.getLogger(__name__)

class WebsiteSender :

    def send(self, weekPrediction):
        self.generateFlyableDays(weekPrediction)
        self.generateAllDays(weekPrediction)
        self.generateSpots()
    
    def generateFlyableDays(self, weekPrediction):
        logger.debug("Start generating markdown for flyableDays")
        flyablesDay = getDaysWithAtLeastOneSlot(weekPrediction)
        sortedPrediction = sortByDate(flyablesDay)

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

        sortedPrediction = sortByDate(weekPrediction)

        file_loader = FileSystemLoader('src/templates')
        env = Environment(loader=file_loader)
        template = env.get_template('all.j2')
        template.globals['now'] = datetime.now().strftime('%A %d %B %H:%M')
        output = template.render(weekPrediction=sortedPrediction)

        f = open("all.markdown","w")
        f.write(output)
        f.close()
        logger.debug("Markdown generated")

    def generateSpots(self):
        logger.debug("Start generating markdown for sites")
        
        f = open("spots.json")
        spots = json.loads(f.read())["spots"]
        f.close() 

        for idx, spot in enumerate(spots) :
            if spot.get("excludeDays", None) is None :
                excludeDaysReadable = "Aucune"
            elif len(spot["excludeDays"]) == 7 :
                excludeDaysReadable = "Toute la semaine"
            else :
                excludeDaysReadable = "le " + ", ".join([calendar.day_name[x] for x in spot['excludeDays']])
            spots[idx]['excludeDaysReadable'] = excludeDaysReadable

            if spot.get('monthsToExcludes') is not None :
                excludeMonthsReadable = "toute l'année" if len(spot.get('monthsToExcludes')) == 12 else "pour les mois de " + ", ".join([calendar.month_name[x] for x in spot['monthsToExcludes']])
                spots[idx]['excludeMonthsReadable'] = excludeMonthsReadable

        file_loader = FileSystemLoader('src/templates')
        env = Environment(loader=file_loader)
        template = env.get_template('about.j2')
        output = template.render(spots=spots)

        f = open("about.markdown","w")
        f.write(output)
        f.close()
        logger.debug("Markdown generated")