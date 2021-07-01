#!/usr/bin/python3

import socket
import sys
import time

UDP_IP_ADDRESS = "192.168.1.21"
#passed as an argument 
UDP_PORT_NO = int(sys.argv[1])

#string of 10 characters = 10 bytes 
data="0123456789"
#packet size needed 
#number depends on the size of the packet needed 
number= 5
packet = data * (number)
packet=packet+"12345678"
# print len of packets string to be sure of the data size
print (" len of payload = ") 
print ( len(packet))
#opening socket 
clientSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
payload = packet.encode()

#header = 42 bytes 
#- let us assume that we want to send a packet with size 100 byte = 58 payload+ 42 header with rate 50 Mbps
#- rate in byte = 6.25M byte per second 
#- number of seconds that each packet takes = 100 byte / 6.25MB = 16microsecond 
#x=number of seconds =packetsize(in bytes)/(numberofbytespersecond)

# x = 100 bytes * 8 = 800 bits
# 800 bits / 50 000 000 bits per sec = 0.000016

# bw in mininet in Mbps (bits per second)
#if we want to send packets with 10Mbps rate
#10 * 1000 000 = 10 000 000 bits per second
#having 100 bytes packet
#100*8 = 800 bits
#800 bits / 10 000 000 = 0.00008 seconds for each pkt
#how much time each packet should take?

numofsec = 0
duration = 700
time.sleep(numofsec)

time_start = time.time()

num=0

while time.time() <= (time_start + duration):
	 clientSock.sendto(payload, (UDP_IP_ADDRESS, UDP_PORT_NO))
	 #print(payload)
	 #time.sleep(0.000016)
	 #time.sleep(0.00008)
	 #time.sleep(0.0000053333)
	 #time.sleep(0.000266667) #for 3Mbps
	 time.sleep(0.0004) # for 2Mbps
	 #time.sleep(0.00016)
	 #time.sleep(0.000533333) #for 1.5Mbps
	 #time.sleep(0.0008) # for 1.0Mbps
	 #time.sleep(0.0008)
	 #print("after-sleep")
	 num+=1

print ("num of pkts sent is:", num)
