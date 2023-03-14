import click
from sender.signalSender import SignalSender
from sender.websiteSender import WebsiteSender
from sender.stdoutSender import StdoutSender

class PredictionSender :

    def __init__(self):
        self.sendToSignal = click.get_current_context().params['send_to_signal']
        self.sentToWebsite = click.get_current_context().params['send_to_website']
        self.sendToStdout = click.get_current_context().params['send_to_stdout']
        self.sendNewRegions = click.get_current_context().params['send_to_new_regions']

    def send(self, weekPrediction, htmlName="all.markdown"):
        if self.sendToStdout :
            stdoutSender = StdoutSender()
            stdoutSender.send(weekPrediction)

        if self.sendToSignal:
            signalSender = SignalSender()
            signalSender.send(weekPrediction)
        
        if self.sentToWebsite :
            websiteSender = WebsiteSender()
            websiteSender.send(weekPrediction)
            
        if self.sendNewRegions :
            websiteSender = WebsiteSender()
            websiteSender.sendNewRegions(weekPrediction, htmlName)