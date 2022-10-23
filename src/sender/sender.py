import click
from sender.signalSender import SignalSender
from sender.websiteSender import WebsiteSender
from sender.stdoutSender import StdoutSender

class PredictionSender :

    def __init__(self):
        self.sendToSignal = click.get_current_context().params['send_to_signal']
        self.sentToWebsite = click.get_current_context().params['send_to_website']
        self.sendToStdout = click.get_current_context().params['send_to_stdout']

    def send(self, weekPrediciton):
        if self.sendToStdout :
            stdoutSender = StdoutSender()
            stdoutSender.send(weekPrediciton)

        if self.sendToSignal:
            signalSender = SignalSender()
            signalSender.send(weekPrediciton)
        
        if self.sentToWebsite :
            websiteSender = WebsiteSender()
            websiteSender.send(weekPrediciton)