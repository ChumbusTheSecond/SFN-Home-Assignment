import socket
import pickle
import ssl
import sqlite3

def adjustBackupTime(targetIp, targetTime):
    dbsConnection = sqlite3.connect('NFC - Router Database')
    conCursor = dbsConnection.cursor()
    
    conCursor.execute('SELECT ip_address FROM Router_config')
    rowRetrieval = conCursor.fetchall()
    ipFound = False
    for row in rowRetrieval:
        if row[0] == targetIp:
            ipFound = True
            print("lol")
    if ipFound == False:
        return "Invlaid IP, enter another"
    else:
        conCursor.execute('''       
                UPDATE Router_Config 
                SET date_and_time = "'''+str(targetTime)+'''"
                WHERE ip_address = "'''+str(targetIp)+'''"
            ''')
        dbsConnection.commit()
        return("entry has been updated")
    
def clientSide():
    clientHost = socket.gethostname() #Retrieve the hostname (This command was used instead of an IP address since all scripts are running locally).
    clientPort = 12345                #Specifies the port that is to be used between the MainProgram.py and ManageDevices.py.
    clientSocket = socket.socket()    #Creates the socket that is to be used between the MainProgram.py and ManageDevices.py.
    clientSocket.connect((clientHost, clientPort))
    clientMessage = "start"           #Used to initialize the clientMessage variable.
    
    while clientMessage.lower().strip() != "end":
        clientMessage = input("\nA) Add Router \nB) Delete Router \nC) List Router \nD) Set Backup Time \nE) Set Router Netflow Settings \nF) Remove Router Netflow Settings \nG) Set Router SNMP Settings \nH) Remove Router SNMP Settings \nI) Show Router Config \nJ) Show Changes in Router Config \nK) Display Router Netflow Statistics \nL) Show Router Syslog \n \nSelect Option: ")
        if clientMessage == 'A' or clientMessage == 'a':
            userRouter = input("\nEnter Router Name: ") #Collect router name
            userIP = input("Enter IP Address: ")        #Collect IP
            userName = input("Enter Username: ")        #Collect Username
            userPassword = input("Enter Password: ")    #Collect password
            clientMessage = "A:"+userRouter+","+userIP+","+userName+","+userPassword
            clientSocket.send(clientMessage.encode())
            data = clientSocket.recv(1024).decode()
            print("\nReceived from server: " +data)
            
        elif clientMessage == 'B' or clientMessage == 'b':
            userIpDel = input("\nEnter Router IP: ")
            clientMessage = "B:"+userIpDel
            clientSocket.send(clientMessage.encode())
            data = clientSocket.recv(1024).decode()
            print("\nReceived from server: " + data)
        
        elif clientMessage == 'C' or clientMessage == 'c':
            clientMessage = 'C:'
            clientSocket.send(clientMessage.encode())
            results = pickle.loads(clientSocket.recv(1024))
            for entry in results:
                print("\nRouter name: "+str(entry[0])+" IP: "+str(entry[1])+ " Username: "+str(entry[2])+ " Password: "+str(entry[3])+"\n")
                
        elif clientMessage == 'D' or clientMessage == 'd':
            usrIP = input("Enter IP: ")
            usrDateTime = input("Enter time for backup: ")
            print(adjustBackupTime(usrIP,usrDateTime))
                  
        else:
            break

    clientSocket.close()    
clientSide()


#Make main menu in loop