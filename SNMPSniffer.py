from scapy.all import sniff, IP, TCP , UDP
import socket
from datetime import datetime
import sqlite3     #Import necessary modules
#---------------------------------------------------------------------------------
SNMPHost = socket.gethostname()
SNMPPort = 161
SNMPSocket = socket.socket()
SNMPSocket.bind((SNMPHost, SNMPPort))
SNMPSocket.listen()
packet_count = 0    # Establishes a connection to MainProgram.py through sockets
#---------------------------------------------------------------------------------
dbsConnection = sqlite3.connect('NFC - Router Database')
conCursor = dbsConnection.cursor() # Establishes a connection to the database
#---------------------------------------------------------------------------------
def handle_snmp_trap(packet):
    global packet_count
#---------------------------------------------------------------------------------
    if 'SNMP' in packet and 'SNMP_TRAP' in packet:
        current_time = datetime.now()
        print("SNMP Trap Received:")
        print(packet.show())
        #---------------------------------------------------------------------------------
        print(f"Date/Time: {current_time}")
        print(f"SYSLOG: {src_ip}")
        print(f"LINK UP: {src_ip}")
        print(f"LINK DOWN IP: {dst_ip}")    # Print or use the extracted parameters
#---------------------------------------------------------------------------------
    conCursor.execute('''       
            INSERT INTO Router_SNMP(syslog, link_up, link_down)
            VALUES( "'''+str(current_time)+'''", "'''+str(src_ip)+'''", "'''+str(packet_count)+'''", "'''+str(src_ip)+'''", "'''+str(dst_ip)+'''", "'''+str(protocol)+'''", "'''+str(src_port)+'''", "'''+str(dst_port)+'''")
        ''') # Adds the parameters listed above to the database accordingly
    dbsConnection.commit()
# Set the network interface to sniff on ('virbr0' in this case)
iface = "virbr0"

# Start sniffing with the specified callback function
sniff(filter = 'udp', prn=handle_snmp_trap, iface='virbr0') # Captures udp packets from the virbr0 interface only