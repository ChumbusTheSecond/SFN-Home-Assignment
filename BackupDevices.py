import socket
import sqlite3
from datetime import datetime
import time
import paramiko

dbsConnection = sqlite3.connect('NFC - Router Database')
conCursor = dbsConnection.cursor()


def databaseBackup():

   while True:
        backuptime = "13:00"
        time.sleep(60)  #Countdown in seconds for checking time in database.
        currTime = datetime.now()   #Gets current time
        finTime = currTime.strftime("%H:%M")    #formats datetime.now into hours and minute
        conCursor.execute('SELECT * FROM Router_Config')
        dateTimeFetch = conCursor.fetchall()
        for row in dateTimeFetch:   #Goes through every row in the table
            if row[1] == finTime:    #if time in database matches with current time
                userConn = paramiko.SSHClient() #Creates paramiko instance
                userConn.set_missing_host_key_policy(paramiko.AutoAddPolicy()) #Yes
                userConn.connect(row[0], '22', 'cisco', 'cisco')    #Connects to the router on GNS and uses the required credentials
                
                stdin, stdout, stderr = userConn.exec_command('show run') #Used to execute the show running-config command on the router
                stdin.close()
                output = stdout.readlines() #gathers the output
                type(output)

                f = open(row[0]+".config", "a") #Creates the .config file required
                for row2 in output:
                    f.write(row2)   #Writes the gathered output line by line in the created config file
                f.close()
                
                print ("\n the config has been saved for router "+row[0]+" \n")
databaseBackup()