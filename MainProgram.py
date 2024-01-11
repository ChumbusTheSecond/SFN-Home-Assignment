import socket
import pickle
import ssl

def clientSide():
    clientHost = socket.gethostname() #Retrieve the hostname (This command was used instead of an IP address since all scripts are running locally).
    clientPort = 12345                #Specifies the port that is to be used between the MainProgram.py and ManageDevices.py.
    clientSocket = socket.socket()    #Creates the socket that is to be used between the MainProgram.py and ManageDevices.py.
    clientSocket.connect((clientHost, clientPort))
    clientMessage = "start"           #Used to initialize the clientMessage variable.
    
    while clientMessage.lower().strip() != "end":
        clientMessage = input("\nA) Add Router \nB) Delete Router \nC) List Router \nSelect option: ")
        if clientMessage == 'A' or clientMessage == 'a':
            userRouter = input("\nEnter Router Name:") #Collect router name
            userIP = input("Enter IP Address:")        #Collect IP
            userName = input("Enter Username:")        #Collect Username
            userPassword = input("Enter Password:")    #Collect password
            clientMessage = "A:"+userRouter+","+userIP+","+userName+","+userPassword
            clientSocket.send(clientMessage.encode())
            data = clientSocket.recv(1024).decode()
            print("\nReceived from server: " +data)
            
        elif clientMessage == 'B' or clientMessage == 'b':
            userIpDel = input("Enter Router IP: ")
            clientMessage = "B:"+userIpDel
            clientSocket.send(clientMessage.encode())
            data = clientSocket.recv(1024).decode()
            print("\nReceived from server: " + data)
        
        elif clientMessage == 'C' or clientMessage == 'c':
            clientMessage = 'C:'
            clientSocket.send(clientMessage.encode())
            results = pickle.loads(clientSocket.recv(1024))
            for entry in results:
                print("Router name: "+str(entry[0])+" IP: "+str(entry[1])+ " Username: "+str(entry[2])+ " Password: "+str(entry[3])+"\n")
        
    clientSocket.close()    
clientSide()


#Make main menu in loop