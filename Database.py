import sqlite3

Connection = sqlite3.connect('NFC - Cisco Router Database')
c = Connection.cursor()

c.execute('''
          CREATE TABLE IF NOT EXISTS Router Information
          ([router_id] INTEGER PRIMARY KEY, [router_name] TEXT, [ip_address] INTEGER, [username] TEXT, [password] TEXT)
          ''')

Connection.commit()