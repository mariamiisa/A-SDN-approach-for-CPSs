from minicps.devices import PLC
from utils1 import *

import time
from threading import Thread

import socket
import json
import select
import logging

PLC201_ADDR = IP['plc201']

Q201 = ('Q201', 1)

class PSocket(Thread):
    """ Class that receives water level from the water_tank.py  """

    def __init__(self, plc_object):
        Thread.__init__(self)
        self.plc = plc_object
	self.q201 = 0

    def run(self):
        print "DEBUG entering socket thread run"
        self.sock = socket.socket()     # Create a socket object
        self.sock.bind((IP['q201'] , 7842 ))
        self.sock.listen(5)

        while True:
            try:
                client, addr = self.sock.accept()
                data = client.recv(4096)                # Get data from the client

                message_dict = eval(json.loads(data))
                self.q201 = float(message_dict['Variable'])

                #print "received from PLC101!", self.q201
                logging.debug('Q1 level received from plc is %s', self.q201)
		self.plc.set(Q201, self.q201)

            except KeyboardInterrupt:
                print "\nCtrl+C was hitten, stopping server"
                client.close()
                break

class PP201(PLC):
        def pre_loop(self, sleep=0.1):
                print 'DEBUG: q201 enters pre_loop'
                time.sleep(sleep)
                logging.basicConfig(filename="q201.log", level=logging.DEBUG)

        def main_loop(self):
                print 'DEBUG: q201 enters main_loop'
                psocket = PSocket(self)
                psocket.start()

if __name__ == '__main__':
	q201 = PP201(name='q201',state=STATE,protocol=Q201_PROTOCOL,memory=GENERIC_DATA,disk=GENERIC_DATA)
