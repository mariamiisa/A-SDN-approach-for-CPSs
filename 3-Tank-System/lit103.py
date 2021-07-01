"""
Sensor 3
Reads water level of Tank3 from database
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

SENSOR_ADDR = IP['lit103']
LIT101 = ('LIT101', 1)
LIT102 = ('LIT102', 1)
LIT103 = ('LIT103', 1)


class SSocket(Thread):
    """ Class that sends water level to the plc  """

    def __init__(self, plc_object):        
        Thread.__init__(self)
        self.plc = plc_object
        self.lit103 = 0

    def run(self):
        print "DEBUG entering socket thread run"
        self.sock = socket.socket()     # Create a socket object    
        self.sock.bind((IP['lit103'] , 8754 ))
        self.sock.listen(5)

        while True:
            try:
                client, addr = self.sock.accept()
                self.lit103 = float(self.plc.get(LIT103))
                msg_dict = dict.fromkeys(['Type', 'Variable'])
                msg_dict['Type'] = "Report"
                msg_dict['Variable'] = self.lit103
                self.lit103 = json.dumps(str(msg_dict))
                
                #print "The value to be sent is ", self.lit102
                logging.debug('LIT103 level to be sent to plc is %s', self.lit103)
                client.send(self.lit103.encode())
		
            except KeyboardInterrupt:
                print "\nCtrl+C was hitten, stopping server"
                client.close()
                break
 

class Lit103(PLC):
    def sigint_handler(self, sig, frame):
        print "I received a SIGINT!"
        sys.exit(0)

    def pre_loop(self, sleep=0.1):
        signal.signal(signal.SIGINT, self.sigint_handler)
        signal.signal(signal.SIGTERM, self.sigint_handler)
        logging.basicConfig(filename=LOG_LIT103_FILE, level=logging.DEBUG)

    def main_loop(self):
        #count = 0
        #time.sleep(0.0005)
        lit = SSocket(self)
        lit.start()
        
if __name__ == '__main__':
    lit103 = Lit103(name='lit102',state=STATE,protocol=LIT103_PROTOCOL,memory=GENERIC_DATA,disk=GENERIC_DATA)
