import sqlite3

dbsConnection = sqlite3.connect('NFC - Router Database')
conCursor = dbsConnection.cursor()

conCursor.execute('''CREATE TABLE IF NOT EXISTS Router_Information
          ([router_id] INTEGER PRIMARY KEY AUTOINCREMENT, [router_name] TEXT, [ip_address] INTEGER, [username] TEXT, [password] TEXT)
          ''')
dbsConnection.commit()