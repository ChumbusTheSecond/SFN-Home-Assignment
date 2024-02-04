#--------------------------------------------------------------------
import socket           #Import necessary modules
import pickle
import sqlite3
#--------------------------------------------------------------------
dbsConnection = sqlite3.connect('NFC - Router Database')   
conCursor = dbsConnection.cursor()  #Establishes a connection with the database
#--------------------------------------------------------------------
def addDevice(routerName, ipAddress, username, password):
    conCursor.execute('SELECT ip_address FROM Router_Information')  #Selects the IP addresses from the Table
    rowRetrieval = conCursor.fetchall()     #Retreives all data from Router_information
    for row in rowRetrieval:
        if str(row[0]) == str(ipAddress):   #If an IP address is already in the database, it will ask the user to enter another IP
            print("already added ERORR")
            return "This IP address is already in use. Try another one."    #Verification failed, returning to main menu.                                                                      
    conCursor.execute('''       
                INSERT INTO Router_Information(router_name,ip_address,username,password)
                VALUES( "'''+str(routerName)+'''", "'''+str(ipAddress)+'''", "'''+str(username)+'''", "'''+str(password)+'''")
              ''')
    dbsConnection.commit()  #If the IP address is not in the table, it will be added to the table with the details provided
    return " \nEntry has been added"
#--------------------------------------------------------------------    
def deleteDevice(ipAddress):
    conCursor.execute('''
            DELETE FROM Router_Information
            WHERE ip_address = "'''+str(ipAddress)+'''"
          ''')
    dbsConnection.commit()  #Deletes the row that includes the IP address given by the user
    return "\nEntry has been deleted"
#--------------------------------------------------------------------
def listDevices():
    conCursor.execute('SELECT router_name,ip_address,username,password FROM Router_Information')
    rowRetrieval = conCursor.fetchall()
    print (rowRetrieval)    #Retreives all the entries present from the Router_Information table
    return rowRetrieval
#--------------------------------------------------------------------
def serverSide():
    serverHostName = socket.gethostname()
    serverPort = 12345
    serverSocket = socket.socket()
    serverSocket.bind((serverHostName, serverPort))
    serverSocket.listen()
    clientIncoming, clientAddress = serverSocket.accept()   #Establishes a connection to MainProgram.py through sockets
    #--------------------------------------------------------------------
    while True:
        clientInput = clientIncoming.recv(1024).decode()    #Decodes incoming messages from MainProgram.py using 1024 bits
        if not clientInput:
            break
        
        clientInputSplit = clientInput.split(":")
        clientInputParameters = clientInputSplit[1].split(",")  #Splits the user message to take only the options A,B or C
        print(clientInputSplit[0]) 
        
        if clientInputSplit[0] == 'A' or clientInputSplit[0] == 'a':
            print("The client has chosen option A")
            print(clientInputSplit[1])
            clientIncoming.send(addDevice(clientInputParameters[0],clientInputParameters[1],clientInputParameters[2],clientInputParameters[3]).encode())    #Sends the inputs to the user in MainProgram.py
            
        elif clientInputSplit[0] == 'B'or clientInputSplit[0] == 'b':
            print("\nUser has chosen option B\n")
            print(clientInputSplit[1])
            clientIncoming.send(deleteDevice(clientInputSplit[1]).encode()) #Sends the IP address parameter from the user in MainProgram.py 
            
        elif clientInputSplit[0] == 'C' or clientInputSplit[0] == 'c':
            print("\nUser has chosen option C\n")
            print(clientInputSplit[1])            
            listEntries=pickle.dumps(listDevices())
            clientIncoming.send(listEntries)            #Sends all entries from the database table to the user in MainProgram.py
    clientIncoming.close()
serverSide()