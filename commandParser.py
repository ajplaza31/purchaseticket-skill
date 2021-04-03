import sqlite3
from sqlite3 import Error
import random
#from RequestHandler import *
#from database import *

def create_connection(path):
	  connection = None
	  try:
		  connection = sqlite3.connect(path)
		  return connection
	  except Error as e:
		  print(e)
	  return connection
  
cubicdb = "cubic.sql"
conn = create_connection(cubicdb)  

def listTickets():
    cur = conn.cursor()
  
    #select and fetch all ticket entries from the table
    cur.execute("SELECT * FROM PassData")
    rows = cur.fetchall()

    print("Available Tickets:\n")
    
    #output all available tickets
    i = 1
    for row in rows:
        #get ETA from transit table using foreign keys
        cur.execute("SELECT * FROM TransitLine WHERE LineID = ?", (row[3],))
        idrow = cur.fetchone()
        print(" %d. Start: %-*s  End: %-*s  ETA: %-*s  Cost: $%s\n" % (i, 20, row[4], 20, row[5], 20, idrow[3], row[6]))
        i += 1
#listTickets()

def getTicket():
    """function that prints out information about a ticket that the user wants"""
    
    cur = conn.cursor()

    listTickets()

    choice = int(input("Which ticket would you like to select? \n"))
    ticketnum = choice
    choice = choice - 1

    cur.execute("SELECT * FROM PassData LIMIT 1 OFFSET ?", (choice,))
    ticket = cur.fetchone()

    cur.execute("SELECT * FROM TransitLine WHERE LineID = ?", (ticket[3],))

    idrow = cur.fetchone()

    print("Here is your ticket information: \n")
    print(" %d. Start: %-*s  End: %-*s  ETA: %-*s  Cost: $%s\n" % (ticketnum, 20, ticket[4], 20, ticket[5], 20, idrow[3], ticket[6]))
    
    

  #return None

def getRoute():
  return None

def purchaseTicket():
  cur = conn.cursor()

  listTickets()

  n = int(input("Which ticket would you like to select? \n"))
  m = n
  n = n - 1

  cur.execute("SELECT * FROM PassData LIMIT 1 OFFSET ?", (n,))
  ticket = cur.fetchone()

  cur.execute("SELECT * FROM TransitLine WHERE LineID = ?", (ticket[3],))

  idrow = cur.fetchone()

  print("You are about to purchase the following ticket: \n")
  print(" %d. Start: %-*s  End: %-*s  ETA: %-*s  Cost: $%s\n" % (m, 20, ticket[4], 20, ticket[5], 20, idrow[3], ticket[6]))
  answer = input("Would you like to proceed? (y/n)\n ")
    
  cardNo = 0
  if (answer == "y"):
  cardNo = (int)(input("Please enter your credit card number: \n"))

  cur.execute("SELECT * FROM Customer WHERE SavedPaymentInfo = ?", (cardNo,))
  savedNo = cur.fetchone()
  choice = ""

  if (savedNo != None):
    print("Thank you for purchasing! \n")
  elif (savedNo == None):
    choice = input("Would you like to save your payment info? (y/n)\n")

  if (choice == "y"):
    name = input("What is your name? \n")
    customerNo = random.randint(11,10000)
    cur.execute("INSERT INTO Customer(CustomerID, SavedPaymentInfo, Name) VALUES(?, ?, ?)", (customerNo, cardNo, name))
    conn.commit()
    print("Thank you for purchasing!\n")
  elif (choice == "n"):
    print("Thank you for purchasing!\n")

      
      
    
    

def execute(cmd):
    if (cmd == "listTickets"):
      listTickets()
    if (cmd == "getTicket"):
      getTicket()
    if (cmd == "getRoute"):
      getRoute()
    if (cmd == "purchaseTicket"):
      purchaseTicket()

print("Available commands:\n")
print("listTickets\n")
print("getTicket\n")
print("getRoute\n")
print("purchaseTicket\n")

while True:
  execute(input())

