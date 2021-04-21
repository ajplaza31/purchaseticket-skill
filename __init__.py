from mycroft import MycroftSkill, intent_file_handler
import sqlite3
import random
import time
from collections import deque

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

        #ticketlist = deque([])
        
        i=1

        for row in rows:
            cur.execute("SELECT * FROM TransitLine WHERE LineID = ?", (row[3],))
            idrow = cur.fetchone()
            self.speak('Ticket {} starts at {}, ends at {}, has an E.T.A of {}, and costs ${}.'.format(i, row[4], row[5], idrow[3], row[6]))
            #ticketNo = "Ticket " + str(i)
            #ticketlist.append(ticketNo)
            i += 1
        
        answer = "no"
        while (answer == "no"):
            #pickedTicket = self.ask_selection(list(ticketlist), 'Which ticket would you like to select?')
            #m = ticketlist.index(pickedTicket) + 1
            n = (int)(self.get_response('Which ticket would you like to select? '))
            m = n
            n = n - 1

            cur.execute("SELECT * FROM PassData LIMIT 1 OFFSET ?", (n,))
            ticket = cur.fetchone()

            cur.execute("SELECT * FROM TransitLine WHERE LineID = ?", (ticket[3],))

            idrow = cur.fetchone()

            self.speak('You are about to purchase the following ticket: \n')
            self.speak(' {}. Start: {},  End: {},  ETA: {},  Cost: ${}.'.format(m, ticket[4], ticket[5], idrow[3], ticket[6]))
            answer = self.ask_yesno("Would you like to proceed? (yes/no) ")
    
            idNumber = 0
            isValid = 0
            #cardNo = 0
            if (answer == "yes"):
                while (isValid == 0):
                    idNumber = (int)(self.get_response('What is your Customer ID? '))

                    cur.execute("SELECT * FROM Customer WHERE CustomerID = ?", (idNumber,))
                    customer = cur.fetchone()

                    if (customer != None):
                        self.speak('Purchasing ticket from {} to {} for ${}'.format(ticket[4], ticket[5], ticket[6]))
                        newBalance = customer[3] - ticket[6]
                        self.speak('Your new account balance is ${}'.format(newBalance))
                        cur.execute('UPDATE Customer SET Balance = ? WHERE CustomerID =?', (newBalance, idNumber))
                        conn.commit()
                        isValid = 1
                        break
                    elif (customer == None):
                        self.speak('That ID is not in the system. Please try again')
                
                self.speak('Thank you for purchasing! ')
                break
            
        conn.close()
        #self.speak_dialog('purchaseticket')


def create_skill():
    return Purchaseticket()

