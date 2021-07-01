"""
Sensor 1
Reads water level of Tank1 from database 
Listens for plc requests
Sends the values by plc request
""" 

from minicps.devices import PLC
from threading import Thread
from utils import *
import random
import logging
import time
import socket 
import json 
import select
import signal
import sys

SENSOR_ADDR = IP['lit101']
LIT101 = ('LIT101', 1)
LIT102 = ('LIT102', 1)

class SSocket(Thread):
    """ Class that sends water level to the plc  """

    def __init__(self, plc_object):        
        Thread.__init__(self)
        self.plc = plc_object
	self.lit101 = 0

    def run(self):
        print "DEBUG entering socket thread run"
        self.sock = socket.socket()     # Create a socket object    
        self.sock.bind((IP['lit101'] , 8754 ))
        self.sock.listen(5)

        while True:
            try:
                client, addr = self.sock.accept()
                
                #self.lit101 = self.plc.get(LIT101)
                self.lit101 = float(self.plc.get(LIT101))
                
                msg_dict = dict.fromkeys(['Type', 'Variable'])
                msg_dict['Type'] = "Report"
                msg_dict['Variable'] = self.lit101
                self.lit101 = json.dumps(str(msg_dict))
                
                #print "The value to be sent is ", self.lit101
                logging.debug('LIT101 level to be sent to plc is %s', self.lit101)
                #self.sock.send(self.lit101)
                client.send(self.lit101.encode())
		
    
            except KeyboardInterrupt:
                print "\nCtrl+C was hitten, stopping server"
                client.close()
                break
 
class Lit101(PLC):
    def sigint_handler(self, sig, frame):
        print "I received a SIGINT!"
        sys.exit(0)

    def pre_loop(self, sleep=0.1):
        signal.signal(signal.SIGINT, self.sigint_handler)
        signal.signal(signal.SIGTERM, self.sigint_handler)
        logging.basicConfig(filename=LOG_LIT101_FILE, level=logging.DEBUG)

    def main_loop(self):
        #count = 0
        #time.sleep(0.0005)
        lit = SSocket(self)
        lit.start()

if __name__ == '__main__':
    lit101 = Lit101(name='lit101',state=STATE,protocol=LIT101_PROTOCOL,memory=GENERIC_DATA,disk=GENERIC_DATA)
