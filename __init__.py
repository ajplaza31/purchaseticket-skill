from mycroft import MycroftSkill, intent_file_handler


class Purchaseticket(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('purchaseticket.intent')
    def handle_purchaseticket(self, message):
        self.speak_dialog('purchaseticket')


def create_skill():
    return Purchaseticket()

