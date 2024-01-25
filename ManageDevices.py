import socket 
import pickle
import sqlite3
import ssl

dbsConnection = sqlite3.connect('NFC - Router Database')
conCursor = dbsConnection.cursor()


def addDevice(routerName, ipAddress, username, password):
    conCursor.execute('SELECT ip_address FROM Router_Information')
    rowRetrieval = conCursor.fetchall()
    for row in rowRetrieval:
        if str(row[0]) == str(ipAddress):
            print("already added ERORR")
            return "This IP address is already in use. Try another one."    #Verification failed, returning to main menu.                                                                      
    conCursor.execute('''       
                INSERT INTO Router_Information(router_name,ip_address,username,password)
                VALUES( "'''+str(routerName)+'''", "'''+str(ipAddress)+'''", "'''+str(username)+'''", "'''+str(password)+'''")
              ''')
    dbsConnection.commit()
    return " \nEntry has been added"
    
def deleteDevice(ipAddress):
    conCursor.execute('''
            DELETE FROM Router_Information
            WHERE ip_address = "'''+str(ipAddress)+'''"
          ''')
    dbsConnection.commit()
    return "\nEntry has been deleted"

def listDevices():
    conCursor.execute('SELECT router_name,ip_address,username,password FROM Router_Information')
    rowRetrieval = conCursor.fetchall()
    print (rowRetrieval)
    return rowRetrieval

def serverSide():
    serverHostName = socket.gethostname()
    serverPort = 12345
    serverSocket = socket.socket()
    serverSocket.bind((serverHostName, serverPort))
    serverSocket.listen()
    clientIncoming, clientAddress = serverSocket.accept()
    
    while True:
        clientInput = clientIncoming.recv(1024).decode()
        if not clientInput:
            break
        
        clientInputSplit = clientInput.split(":")
        clientInputParameters = clientInputSplit[1].split(",")
        print(clientInputSplit[0])
        
        if clientInputSplit[0] == 'A' or clientInputSplit[0] == 'a':
            print("The client has chosen option A")
            print(clientInputSplit[1])
            clientIncoming.send(addDevice(clientInputParameters[0],clientInputParameters[1],clientInputParameters[2],clientInputParameters[3]).encode())
            
        elif clientInputSplit[0] == 'B'or clientInputSplit[0] == 'b':
            print("\nUser has chosen option B\n")
            print(clientInputSplit[1])
            clientIncoming.send(deleteDevice(clientInputSplit[1]).encode())
            
        elif clientInputSplit[0] == 'C' or clientInputSplit[0] == 'c':
            print("\nUser has chosen option C\n")
            print(clientInputSplit[1])
            #clientIncoming.send(listDevices().encode())            
            listEntries=pickle.dumps(listDevices())
            clientIncoming.send(listEntries)
    clientIncoming.close()
serverSide()