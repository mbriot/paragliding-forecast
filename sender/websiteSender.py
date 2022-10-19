import logging
from datetime import datetime
from jinja2 import Environment, FileSystemLoader

logger = logging.getLogger(__name__)

class WebsiteSender :

    def send(self, weekPrediction):
        logger.debug("Start generating markdown")
        
        sortedPrediction = {}
        for date in sorted(weekPrediction.keys()):
            sortedPrediction[datetime.fromtimestamp(int(date)).strftime('%A %d %B')] = weekPrediction[date]        

        file_loader = FileSystemLoader('templates')
        env = Environment(loader=file_loader)
        template = env.get_template('index.j2')
        template.globals['now'] = datetime.now().strftime('%A %d %B %H:%M')
        output = template.render(weekPrediction=sortedPrediction)

        f = open("index.markdown","w")
        f.write(output)
        f.close()
        logger.debug("Markdown generated")