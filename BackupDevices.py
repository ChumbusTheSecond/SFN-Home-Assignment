import socket
import os
import sqlite3
from datetime import datetime
import time
from netmiko import ConnectHandler
from github import Github   # Import the necessary modules

def databaseBackup():
    #---------------------------------------------------------------------------------------------------------------------
    cmdOutput=""
    presentFile=""
    while True:
        time.sleep(60) # Timer was set to 5 for testing
        currentTime = datetime.now()
        hrsMin = currentTime.strftime("%H:%M")  # Takes the current time and turns into hours and minutes
        #----------------------------------------------------------------------------------------------------------------
        dbsConnection = sqlite3.connect('NFC - Router Database')
        conCursor = dbsConnection.cursor()
        conCursor.execute('SELECT * FROM Router_Config')
        fetchDetails = conCursor.fetchall()     # Connects to the database and selects everything from the table Router_Config
        #----------------------------------------------------------------------------------------------------------------
        for row in fetchDetails:
            if hrsMin == hrsMin:    # This is supposed to be hrsMin == row[1], it was proven to work, however for some unknown reason it failed afterwards
                cisco_881 = {'device_type': 'cisco_ios','host': row[0],'username': 'cisco','password': 'cisco','port': '22'}
                net_connect = ConnectHandler(**cisco_881)
                shRunCmds = ['exit','show run',' ',' ',' ']
                cmdOutput = net_connect.send_config_set(shRunCmds)
                print(cmdOutput)    # Initiates an SSH connection to the router that is present in the database and sends the commands for show run and then prints the output in the terminal
        #----------------------------------------------------------------------------------------------------------------
        desktop_path = os.path.expanduser("~/Desktop")  # Saves the config file in the Desktop directory
        f = open(os.path.join(desktop_path,row[0]+".config"), "a") # Creates the .config file required
        for row2 in cmdOutput:
            f.write(row2)   # Writes the gathered output line by line in the created config file
        f.close()    
        print ("\n the config has been saved for router "+row[0]+" \n")
        #----------------------------------------------------------------------------------------------------------------
        gitToken = Github('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')   # Github token
        repos = gitToken.get_repo('ChumbusTheSecond/BackupDevicesRep.') # Github account w/ repository name
        filePath = 'Desktop/192.168.122.40.config'                      # Path and name of file to be uploaded
        with open(filePath, 'r') as file:
            data = file.read()
        uploadFile = 'home/192.168.122.40.config'
        mainBranch = 'main'                                             # Identifies the branch
        try:       # Check if the file already exists
            presentFile = repos.get_contents(filePath, ref=mainBranch)
            repos.update_file(presentFile.path, 'Update file', data, presentFile.sha, branch=mainBranch) # Update the existing file
            print(f'File "{uploadFile}" updated successfully.')
        except Exception as e:
            repos.create_file(filePath, 'Create file', data, branch=mainBranch)    # If the file does not exist, create a new file
            print(f'File uploaded successfully.')
        #----------------------------------------------------------------------------------------------------------------
databaseBackup()