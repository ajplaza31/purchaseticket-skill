from mycroft import MycroftSkill, intent_file_handler
import sqlite3
import random

class Purchaseticket(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self) 

    @intent_file_handler('purchaseticket.intent')
    def handle_purchaseticket(self, message):
        conn = sqlite3.connect("cubic.sql") 
        cur = conn.cursor()
    
        cur.execute("SELECT * FROM PassData")
        rows = cur.fetchall()

        self.speak('Here are the available tickets.')

        ticketlist = []
        
        i=1

        for row in rows:
            cur.execute("SELECT * FROM TransitLine WHERE LineID = ?", (row[3],))
            idrow = cur.fetchone()
            self.speak('Ticket {} starts at {}, ends at {}, has an E.T.A of {}, and costs ${}.'.format(i, row[4], row[5], idrow[3], row[6]))
            ticketNo = "Ticket " + str(i)
            ticketlist.append(ticketNo)
            i += 1

        pickedTicket = self.ask_selection(ticketlist, 'Which ticket would you like to select?')
        m = ticketlist.index(pickedTicket) + 1

        cur.execute("SELECT * FROM PassData LIMIT 1 OFFSET ?", (ticketlist.index(pickedTicket),))
        ticket = cur.fetchone()

        cur.execute("SELECT * FROM TransitLine WHERE LineID = ?", (ticket[3],))

        idrow = cur.fetchone()

        self.speak('You are about to purchase the following ticket: \n')
        self.speak(' {}. Start: {},  End: {},  ETA: {},  Cost: ${}.'.format(m, ticket[4], ticket[5], idrow[3], ticket[6]))
        answer = self.ask_yesno("Would you like to proceed? (yes/no) ")
    
        cardNo = 0
        if (answer == "yes"):
            cardNo = self.get_response('Please enter your credit card number: ')

        cur.execute("SELECT * FROM Customer WHERE SavedPaymentInfo = ?", (cardNo,))
        savedNo = cur.fetchone()
        choice = ""

        if (savedNo != None):
            choice = self.ask_yesno("Would you like to save your payment info? (y/n)")
        elif (savedNo == None):
            self.speak("Thank you for purchasing!")

        if (choice == "yes"):
            name = self.get_response("What is your name? \n")
            customerNo = random.randint(11,10000)
            cur.execute("INSERT INTO Customer(CustomerID, SavedPaymentInfo, Name) VALUES(?, ?, ?)", (customerNo, cardNo, name))
            conn.commit()
            self.speak("Thank you for purchasing!")
        elif (choice == "no"):
            self.speak("Thank you for purchasing!")

        conn.close()
        #self.speak_dialog('purchaseticket')


def create_skill():
    return Purchaseticket()

