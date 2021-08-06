""" PLC 2 """

from minicps.devices import PLC
from threading import Thread
from utils1 import *
from random import *

import json
import select
import socket
import time
import signal
import sys

Q201 = ('Q201', 1)
Q202 = ('Q202', 1)

LIT201 = ('LIT201', 1)
LIT202 = ('LIT202', 1)
LIT203 = ('LIT203', 1)

SENSOR_ADDR = IP['lit201']
IDS_ADDR = IP['ids101']

#received_lit101 = 0
#received_lit102 = 0

#lit103 = Y30
#lit103_prev = Y30

class Lit301Socket(Thread):
    """ Class that receives water level from the water_tank.py  """

    def __init__(self, plc_object):
        Thread.__init__(self)
        self.plc = plc_object

    def run(self):
        #print "DEBUG entering socket thread run"
        self.sock = socket.socket()     # Create a socket object
        self.sock.bind((IP['plc201'] , 8754 ))
        self.sock.listen(5)

        while (self.plc.count <= PLC_SAMPLES):
            try:
                client, addr = self.sock.accept()
                data = client.recv(4096)        # Get data from the client
                message_dict = eval(json.loads(data))
                lit203 = float(message_dict['Variable']) - lit203_prev
                lit203_prev = lit203

            except KeyboardInterrupt:
                print "\nCtrl+C was hitten, stopping server"
                client.close()
                break

class PLC201(PLC):

    def send_message(self, ipaddr, port, message):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((ipaddr, port))

        msg_dict = dict.fromkeys(['Type', 'Variable'])
        msg_dict['Type'] = "Report"
        msg_dict['Variable'] = message
        message = json.dumps(str(msg_dict))

        try:
            ready_to_read, ready_to_write, in_error = select.select([sock, ], [sock, ], [], 5)
        except:
            print "Socket error"
            return
        if(ready_to_write > 0):
            sock.send(message)
            print "At count ", self.count
            print "Sending to the pump:", message
	    
        sock.close()
        
        
    def recv_message(self, ipaddr, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((ipaddr, port))
        
        try:
            ready_to_read, ready_to_write, in_error = select.select([sock, ], [sock, ], [], 5)
        except:
            print "Socket error"
            return
        if(ready_to_read > 0):

            data = sock.recv(4096)
            
            encoded_data = data.decode()
            message_dict = eval(json.loads(data))
            received_level = float(message_dict['Variable'])
            sock.close()
            print "At count ", self.count
            print "Received level is: ", received_level
            #received = received_level
            return received_level
            


    def change_references(self):

            if self.count <= 50:
                    self.ref_y0 = 0.4
            if self.count > 50 and self.count <= 350:
                    self.ref_y0 = 0.450
            if self.count > 350:
                    self.ref_y0 = 0.4

            if self.count <= 70:
                    self.ref_y1 = 0.2
            if self.count > 70 and self.count <= 400:
                    self.ref_y1 = 0.225
            if self.count > 400:
                    self.ref_y1 = 0.2

    def sigint_handler(self, sig, frame):
        print "I received a SIGINT!"
        sys.exit(0)

    def pre_loop(self, sleep=0.1):
        print 'DEBUG: swat-s1 plc1 enters pre_loop'
        signal.signal(signal.SIGINT, self.sigint_handler)
        signal.signal(signal.SIGTERM, self.sigint_handler)

        # Controller Initial Conditions
        self.count = 0

        self.ref_y0 = Y10
        self.ref_y1 = Y20

        self.lit201 = 0.0
        self.lit202 = 0.0
        lit203 = 0.0
        #self.lit103 = 0.0

        self.q1 = 0.0
        self.q2 = 0.0

        self.received_lit201 = 0.0
        self.received_lit202 = 0.0
        received_lit203 = 0.0
        #self.received_lit103 = 0.0

        self.z =  np.array([[0.0],[0.0]], )
        self.current_inc_i = np.array([[0.0],[0.0]])
        self.K1K2 = np.concatenate((K1,K2),axis=1)

    def main_loop(self):
        """plc1 main loop.
            - reads sensors value
            - drives actuators according to the control strategy
            - updates its enip server
        """

        print 'DEBUG: swat-s1 plc1 enters main_loop.'

        while(self.count <= PLC_SAMPLES):
	    try:

		self.change_references()
		print "Count: ", self.count, "ref_y0: ", self.ref_y0
                print "Q1 value: ", Q1 , "Q2 value: " , Q2
		
		
		self.received_lit201 = self.recv_message(IP['lit201'], 8754)
		self.received_lit202 = self.recv_message(IP['lit202'], 8754)
		#self.received_lit103 = self.recv_message(IP['lit103'], 8754)
		
		#print "The received levels from the sensors are: ", self.received_lit101, self.received_lit102
		
		#self.received_lit101 = float(self.receive(LIT101, SENSOR_ADDR))
		#self.received_lit101 = float(self.get(LIT101))
	    	self.lit201 = self.received_lit201 - Y10

		#xhat is the vector used for the controller. In the next version, xhat shouldn't be read from sensors, but from luerenberg observer
		#self.received_lit102 = float(self.get(LIT102))
		self.lit202 = self.received_lit202 - Y20

		received_lit203 = float(self.get(LIT203))
		lit203 = received_lit203 - Y30
		#self.lit103 = self.received_lit103 - Y30

		self.lit201_error = self.ref_y0 - self.received_lit201
		self.lit202_error = self.ref_y1 - self.received_lit202
		#print "Error: ", self.lit101_error, " ", self.lit102_error

		#print lit101, lit102,lit103
		#set sequence numbers

		# Z(k+1) = z(k) + error(k)
		
		
		self.z[0,0] = self.z[0,0] + self.lit201_error
		self.z[1,0] = self.z[1,0] + self.lit202_error

		# xhat should be xhat(t) = xhat(t) - xhat(-1)
		self.xhat= np.array([[self.lit201],[self.lit202],[lit203]])
		self.xhatz=np.concatenate((self.xhat,self.z), axis=0)
		#print "xhatz: ", self.xhatz

		self.current_inc_i = np.matmul(-self.K1K2,self.xhatz)

		self.q1 = Q1 + self.current_inc_i[0]
		self.q2 = Q2 + self.current_inc_i[1]
		#print "Cumulative inc: ", " ", self.current_inc_i[0], " ", self.current_inc_i[1]
		#print "Sending to actuators: ", " ", self.q1, " ", self.q2

		#self.set(Q101, float(self.q1))
		#self.set(Q102, float(self.q2))
                self.send_message(IP['q201'], 7842 ,float(self.q1))
                self.send_message(IP['q202'], 7842 ,float(self.q2))

		#print "Sending to q101:", self.q1
		#print "Sending to q102:", self.q2

		self.count += 1
		time.sleep(PLC_PERIOD_SEC)

		# Nos hace falta definir antes del loop el vector con los valores de referencia (numpy.zeros inicializa un arreglo con 0 del tamano deseado)

	    except Exception as e:
                   print e
		   print "Switching to backup"
		   break


if __name__ == "__main__":

    plc201 = PLC201(name='plc201',state=STATE,protocol=PLC201_PROTOCOL,memory=GENERIC_DATA,disk=GENERIC_DATA)
