import socket
import pickle
import ssl
import sqlite3
from scapy.all import *
import paramiko
from netmiko import ConnectHandler
from github import Github   # Imports the necessary modules

def adjustBackupTime(targetIp, targetTime):
    dbsConnection = sqlite3.connect('NFC - Router Database')
    conCursor = dbsConnection.cursor()      # Establishes a connection to the database
    
    conCursor.execute('SELECT ip_address FROM Router_config')
    rowRetrieval = conCursor.fetchall()
    ipFound = False
    for row in rowRetrieval:
        if row[0] == targetIp:
            ipFound = True
            print("lol")        # Retreives the IP addresses from Router_Config, if the IP is found, time is adjusted by the user, if not found, user chooses another IP
    if ipFound == False:
        return "Invlaid IP, enter another"
    else:
        conCursor.execute('''       
                UPDATE Router_Config 
                SET date_and_time = "'''+str(targetTime)+'''"
                WHERE ip_address = "'''+str(targetIp)+'''"
            ''')
        dbsConnection.commit()  # Updates the date and time for the given IP
        return("entry has been updated")
    
def addNetflow():
    userNetFlowIPAdd = input("Enter Router IP to apply Netflow Configuration: ")
    cisco_881 = {'device_type': 'cisco_ios','host': userNetFlowIPAdd,'username': 'cisco','password': 'cisco','port': '22'}
    net_connect=ConnectHandler(**cisco_881)
    config_commands = [ 'ip flow-cache timeout inactive 10','ip flow-cache timeout active 10','ip flow-export source FastEthernet0/0',
                        'ip flow-export version 9','ip flow-export destination 192.168.122.1 2055','interface FastEthernet0/0','ip flow ingress','ip flow egress',
                        'exit','exit','wr mem']
    output = net_connect.send_config_set(config_commands)   # Establishes an SSH connection to the router with the IP address given by the user and sends the netflow configuration commands.
    return("\nNetflow has been configured on this router")
    
def delNetflow():
    userNetFlowIPDel = input("Enter Router IP to apply Netflow Configuration: ")
    cisco_881 = {'device_type': 'cisco_ios','host': userNetFlowIPDel,'username': 'cisco','password': 'cisco','port': '22'}
    net_connect=ConnectHandler(**cisco_881)
    config_commands = ['no ip flow-cache timeout inactive 10','no ip flow-cache timeout active 10','no ip flow-export source FastEthernet0/0','no ip flow-export version 9',
                       'no ip flow-export destination 192.168.122.1 2055','no interface FastEthernet0/0','no ip flow ingress','no ip flow egress',
                       'exit','exit','wr mem']
    output = net_connect.send_config_set(config_commands)   # Establishes an SSH connection to the router with the IP address given by the user and removes the netflow configuration commands.
    print(output)
    return("\nNetflow configuration has been removed from this router")

def addSNMP():
    userSNMPAdd = input("\nEnter Router IP to apply SNMP Configuration: ")
    cisco_881 = {'device_type': 'cisco_ios','host': userSNMPAdd,'username': 'cisco','password': 'cisco','port': '22'}
    net_connect=ConnectHandler(**cisco_881)
    config_commands = ['logging history debugging','snmp-server community SFN RO','snmp-server ifindex persist','snmp-server enable traps snmp linkdown linkup',
                    'snmp-server enable traps syslog','snmp-server enable traps snmp linkdown linkup','snmp-server enable traps syslog','snmp-server host '+ str(userSNMPAdd) + ' version 2c SFN']
    output = net_connect.send_config_set(config_commands)   # Establishes an SSH connection to the router with the IP address given by the user and adds SNMP configuration commands.
    print(output)
    return("\SNMP has been configured for this router")

def delSNMP():
    userSNMPAdd = input("\nEnter Router IP to remove SNMP Configuration: ")
    cisco_881 = {'device_type': 'cisco_ios','host': userSNMPAdd,'username': 'cisco','password': 'cisco','port': '22'}
    net_connect=ConnectHandler(**cisco_881)
    config_commands = ['no logging history debugging','no snmp-server community SFN RO','no snmp-server ifindex persist','no snmp-server enable traps snmp linkdown linkup',
                    'no snmp-server enable traps syslog','no snmp-server enable traps snmp linkdown linkup','no snmp-server enable traps syslog','no snmp-server host '+ str(userSNMPAdd) + ' version 2c SFN']
    output = net_connect.send_config_set(config_commands)   # Establishes an SSH connection to the router with the IP address given by the user and removes the SNMP configuration commands.
    print(output)
    return("\SNMP configuration has been removed for this router")

def listConf():
    gitToken = Github('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')   # Github Token
    repos = gitToken.get_repo('ChumbusTheSecond/BackupDevicesRep.') # Account name w/ repository name
    filePath = 'Desktop/192.168.122.40.config'  # The path of the config file in the repository
    retrFile = repos.get_contents(filePath)     # Gets the content of the config file from the repository
    fileDecode = retrFile.content.decode('utf-8')   # Decodes the file using UTF-8. .decode() does not exist thus it cannot decode the file
    print("192.168.122.40 config file: ")   
    print(fileDecode)

def clientSide():
    clientHost = socket.gethostname() # Retrieve the hostname (This command was used instead of an IP address since all scripts are running locally).
    clientPort = 12345                # Specifies the port that is to be used between the MainProgram.py and ManageDevices.py.
    clientSocket = socket.socket()    # Creates the socket that is to be used between the MainProgram.py and ManageDevices.py.
    clientSocket.connect((clientHost, clientPort))
    clientMessage = "start"           # Used to initialize the clientMessage variable.
    
    while clientMessage.lower().strip() != "end":
        clientMessage = input("\nA) Add Router \nB) Delete Router \nC) List Router \nD) Set Backup Time \nE) Set Router Netflow Settings \nF) Remove Router Netflow Settings \nG) Set Router SNMP Settings \nH) Remove Router SNMP Settings \nI) Show Router Config \nJ) Show Changes in Router Config \nK) Display Router Netflow Statistics \nL) Show Router Syslog \n \nSelect Option: ")
        if clientMessage == 'A' or clientMessage == 'a':
            userRouter = input("\nEnter Router Name: ") # Collect router name
            userIP = input("Enter IP Address: ")        # Collect IP
            userName = input("Enter Username: ")        # Collect Username
            userPassword = input("Enter Password: ")    # Collect password
            
            clientMessage = "A:"+userRouter+","+userIP+","+userName+","+userPassword
            clientSocket.send(clientMessage.encode())   # Sends the  user inputs to ManageDevices.py
            data = clientSocket.recv(1024).decode()     # Receives the response form ManageDevices.py and decodes it
            print("\nReceived from server: " +data)
            
        elif clientMessage == 'B' or clientMessage == 'b':
            userIpDel = input("\nEnter Router IP: ")
            clientMessage = "B:"+userIpDel
            clientSocket.send(clientMessage.encode())   # Sends the  user inputs to ManageDevices.py
            data = clientSocket.recv(1024).decode()     # Receives the response form ManageDevices.py and decodes it
            print("\nReceived from server: " + data)
        
        elif clientMessage == 'C' or clientMessage == 'c':
            clientMessage = 'C:'
            clientSocket.send(clientMessage.encode())   # Sends the user input to ManageDevices.py
            results = pickle.loads(clientSocket.recv(1024))
            for entry in results:
                print("\nRouter name: "+str(entry[0])+" IP: "+str(entry[1])+ " Username: "+str(entry[2])+ " Password: "+str(entry[3])+"\n") # Lists the entries of the table in the database, received from ManageDevices.py
                
        elif clientMessage == 'D' or clientMessage == 'd':
            usrIP = input("Enter IP: ")
            usrDateTime = input("Enter time for backup: ")  # Asks the user to give a time
            print(adjustBackupTime(usrIP,usrDateTime))  # If the user chooses D/d, the function adjustBackupTime() is called
            
        elif clientMessage == 'E' or clientMessage == 'e':
            clientPort == 2055
            addNetflow()
            print("\nNetflow has been configured on this router")    # If the user chooses E/e, the function addNetflow() is called
            
        elif clientMessage == 'F' or clientMessage == 'f':
            clientPort == 2055
            delNetflow()
            print("\nNetflow configuration has been cleared from this router") # If the user chooses F/f, the function delNetflow() is called
                  
        elif clientMessage == 'G' or clientMessage == 'g':
            clientPort == 161
            addSNMP()
            print("\nSNMP has been configured on this router")  # If the user chooses G/g, the function addSNMP() is called
        
        elif clientMessage == 'H' or clientMessage == 'h':
            clientPort == 161
            delSNMP()
            print("\nSNMP has been removed from this router")    #If the user chooses H/h, the function delSNMP() is called
            
        elif clientMessage == 'I' or clientMessage == 'i':
             listConf() #If the user chooses I/i, the function listConf() is called
        else:
            break

    clientSocket.close()
clientSide()