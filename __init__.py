from mycroft import MycroftSkill, intent_file_handler
from src.commandParser import purchaseTicket

class Purchaseticket(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('purchaseticket.intent')
    def handle_purchaseticket(self, message):
        purchaseTicket()
        self.speak_dialog('purchaseticket')


def create_skill():
    return Purchaseticket()

