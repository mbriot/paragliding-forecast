import logging
from datetime import datetime
from jinja2 import Environment, FileSystemLoader

logger = logging.getLogger(__name__)

class WebsiteSender :

    def send(self, weekPrediction):
        logger.debug("je vais faire du html")
        file_loader = FileSystemLoader('templates')
        env = Environment(loader=file_loader)
        template = env.get_template('index.j2')
        template.globals['now'] = datetime.now().strftime('%A %d %B')
        output = template.render(weekPrediction=weekPrediction)

        f = open("index.markdown","w")
        f.write(output)
        f.close()
        print(output)