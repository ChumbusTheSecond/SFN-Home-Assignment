from scapy.all import sniff, IP, TCP , UDP
import socket
from datetime import datetime
import sqlite3     #Import necessary modules
#---------------------------------------------------------------------------------
NetflowHost = socket.gethostname()
NetflowPort = 2055
NetflowSocket = socket.socket()
NetflowSocket.bind((NetflowHost, NetflowPort))
NetflowSocket.listen()
packet_count = 0    # Establishes a connection to MainProgram.py through sockets
#---------------------------------------------------------------------------------
dbsConnection = sqlite3.connect('NFC - Router Database')
conCursor = dbsConnection.cursor() # Establishes a connection to the database
#---------------------------------------------------------------------------------
def packet_callback(packet):
     global packet_count
#---------------------------------------------------------------------------------
     if IP in packet:    # Check if the packet has an IP layer     
        if UDP in packet:     # Check if the packet has a UDP layer
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")    # Extract date and time
            #---------------------------------------------------------------------------------
            src_ip = packet[IP].src      # Extract source IP addresses
            dst_ip = packet[IP].dst      # Extract destination IP address
            #---------------------------------------------------------------------------------
            src_port = packet[UDP].sport     # Extract source port number
            dst_port = packet[UDP].dport     # Extract destination port number
            protocol = "UDP"                 # Extract protocol
            #---------------------------------------------------------------------------------
            print(f"Date/Time: {current_time}")
            print(f"Router IP: {src_ip}")
            print(f"Source IP: {src_ip}")
            print(f"Destination IP: {dst_ip}")
            print(f"Source Port: {src_port}")
            print(f"Destination Port: {dst_port}")
            print(f"Protocol: {protocol}")            # Print or use the extracted parameters
            #---------------------------------------------------------------------------------
            packet_count += 1      # Increment packet count
            print(f"Number of Packets: {packet_count}")
            print("-" * 30)
            #---------------------------------------------------------------------------------
     conCursor.execute('''       
               INSERT INTO Router_NetflowV9(date_and_time, router_ip, number_of_packets, source_ip, destination_ip, protocol, source_port, destination_port)
               VALUES( "'''+str(current_time)+'''", "'''+str(src_ip)+'''", "'''+str(packet_count)+'''", "'''+str(src_ip)+'''", "'''+str(dst_ip)+'''", "'''+str(protocol)+'''", "'''+str(src_port)+'''", "'''+str(dst_port)+'''")
          ''') # Adds the parameters listed above to the database accordingly
     dbsConnection.commit()
     #----------------------------------------------------------------------------------------
sniff(filter = 'udp', prn=packet_callback, iface='virbr0') # Captures udp packets from the virbr0 interface only