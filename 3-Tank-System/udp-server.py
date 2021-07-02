#!/usr/bin/python3
import socket
import sys
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = '192.168.1.21'
#server port is an argument 
server_port = int(sys.argv[1])

server = (server_address, server_port)
sock.bind(server)
print("Listening on " + server_address + ":" + str(server_port))

num=0

while True:
  
	payload, client_address = sock.recvfrom(1000)
	payload2 = payload.decode()
	print("Received data is : " + str(payload))
    
print ("number of received packets = ",num)
