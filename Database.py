import sqlite3  #Imports necessary modules

dbsConnection = sqlite3.connect('NFC - Router Database')
conCursor = dbsConnection.cursor()  #Establishes a connection to the database

conCursor.execute('''CREATE TABLE IF NOT EXISTS Router_Information
          ([router_id] INTEGER PRIMARY KEY AUTOINCREMENT, [router_name] TEXT, [ip_address] INTEGER, [username] TEXT, [password] TEXT)
          ''')  #Creates a table named Router_Information with 5 columns

conCursor.execute('''CREATE TABLE IF NOT EXISTS Router_Config
          ([ip_address] INTEGER, [date_and_time] TEXT)
          ''')  #Creates a table named Router_Config with 2 columns

conCursor.execute('''CREATE TABLE IF NOT EXISTS Router_NetflowV9
          ([date_and_time] TEXT, [router_ip] INTEGER, [number_of_packets] INTEGER, [source_ip] INTEGER, [destination_ip] INTEGER, [protocol] TEXT, [source_port] INTEGER, [destination_port] INTEGER)
          ''')  #Creates a table named Router_NetflowV9 with 8 columns
dbsConnection.commit()

conCursor.execute('''CREATE TABLE IF NOT EXISTS Router_SNMP
          ([syslog] TEXT, [link_up] TEXT, [link_down] TEXT
          ''')  #Creates a table named Router_NetflowV9 with 8 columns
dbsConnection.commit()