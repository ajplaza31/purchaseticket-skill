from mycroft import MycroftSkill, intent_file_handler
import sqlite3

class Purchaseticket(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('purchaseticket.intent')
    def handle_purchaseticket(self, message):
        
        conn = sqlite3.connect("cubic.sql")
        cur = conn.cursor()

        cur.execute("SELECT * FROM PassData")
        rows = cur.fetchall()
        
        i=1
        
        self.speak('Here are the available tickets.')
        
        for row in rows:
            cur.execute("SELECT * FROM TransitLine WHERE LineID = ?", (row[3],))
            idrow = cur.fetchone()
            self.speak('Ticket {} starts at {}, ends at {}, has an E.T.A of {}, and costs {}.'.format(i, row[4], row[5], idrow[3], row[6]))
            i += 1

        n = int(input("Which ticket would you like to select? \n"))
        m = n
        n = n - 1

        cur.execute("SELECT * FROM PassData LIMIT 1 OFFSET ?", (n,))
        ticket = cur.fetchone()

        cur.execute("SELECT * FROM TransitLine WHERE LineID = ?", (ticket[3],))

        idrow = cur.fetchone()

        self.speak("You are about to purchase the following ticket: \n")
        self.speak(" %d. Start: %-*s  End: %-*s  ETA: %-*s  Cost: $%s\n" % (m, 20, ticket[4], 20, ticket[5], 20, idrow[3], ticket[6]))
        answer = input("Would you like to proceed? (y/n)\n ")
    
        cardNo = 0
        if (answer == "y"):
        cardNo = (int)(input("Please enter your credit card number: \n"))

        cur.execute("SELECT * FROM Customer LIMIT 1 OFFSET ?", (n,))
        savedNo = cur.fetchall()
        choice = ""

        if (len(savedNo) == 0):
            choice = input("Would you like to save your payment info? (y/n)\n")
        else:
            self.speak("Thank you for purchasing! \n")

        if (choice == "y"):
            name = input("What is your name? \n")
            customerNo = random.randint(11,10000)
            cur.execute("INSERT INTO Customer(CustomerID, SavedPaymentInfo, Name) VALUES(?, ?, ?)", (customerNo, cardNo, name))
        elif (choice == "n"):
            self.speak("Thank you for purhcasing!\n")

        conn.close()
        #self.speak_dialog('purchaseticket')


def create_skill():
    return Purchaseticket()

