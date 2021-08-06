from minicps.devices import Tank
from minicps.devices import PLC
from scipy.integrate import odeint
from utils1 import *
#from utils import  *
import numpy as np
import sys
import time
import math
import logging
import signal
import sys

Q201 = ('Q201', 1)
Q202 = ('Q202', 1)
LIT201 = ('LIT201', 1)
LIT202 = ('LIT202', 1)
LIT203 = ('LIT203', 1)
PLC_ADDR = IP['plc201']

class RawWaterTank(PLC):

	def sigint_handler(self, sig, frame):
		print "I received a SIGINT!"
		sys.exit(0)

	def plant_model(self, l, t, q):
		MQ1, MQ2 = q
		L1, L2, L3 = l

		# System of 3 differential equations of the water tanks
		f = [(MQ1 - mu13*sn*np.sign(L1-L3)*math.sqrt(2*g*abs(L1-L3)))/s,
		(MQ2 + mu32*sn*np.sign(L3-L2)*math.sqrt(2*g*abs(L3-L2)) - mu20*sn*math.sqrt(2*g*L2))/s,
		(mu13*sn*np.sign(L1-L3)*math.sqrt(2*g*abs(L1-L3)) - mu32*sn*np.sign(L3-L2)*math.sqrt(abs(2*g*abs(L3-L2))))/s
		]

		return f

	def pre_loop(self):
		signal.signal(signal.SIGINT, self.sigint_handler)
		signal.signal(signal.SIGTERM, self.sigint_handler)
		logging.basicConfig(filename="plant.log", level=logging.DEBUG)
		logging.debug('plant enters pre_loop')
		self.Y1= 0.4
		self.Y2= 0.2
		self.Y3= 0.3

		self.set(LIT201, self.Y1)
		self.set(LIT202, self.Y2)
		self.set(LIT203, self.Y3)

		self.Q1 = Q1
		self.Q2 = Q2

		self.set(Q201, self.Q1)
		self.set(Q202, self.Q2)

		# These vectors are used by the model
		self.l = [self.Y1, self.Y2, self.Y3]
		self.abserr = 1.0e-8
		self.relerr = 1.0e-6
		self.lock = 0.0

	def main_loop(self):
		count = 0
		#logging.debug('starting simulation')
		#logging.debug('Initial values: L1: ', self.l[0], ' L2: ', self.l[1], ' L3: ', self.l[2])
		stoptime = 1
		numpoints = 100
		t = [stoptime * float(i) / (numpoints - 1) for i in range(numpoints)]

		while(count <= PP_SAMPLES):
			print count, " ", self.l
			
			#I added the following line
			logging.debug('\nAt count %d ', count)
			
			self.Q1 = float(self.get(Q201))
			self.Q2 = float(self.get(Q202))
			
			#added
			logging.debug('Q1 value read from database is %s ', self.Q1)
			logging.debug('Q2 value read from datavase is %s ', self.Q2)
			
			self.q = [self.Q1, self.Q2]
			wsol = odeint(self.plant_model, self.l, t, args=(self.q,),atol=self.abserr, rtol=self.relerr)

			#print "dl/dt ", wsol

			if (wsol[-1][0]) > 0.62:
				wsol[-1][0] = 0.62

			if (wsol[-1][1]) > 0.62:
				wsol[-1][1] = 0.62

			if (wsol[-1][2]) > 0.62:
				wsol[-1][2] = 0.62

			self.l=[wsol[-1][0], wsol[-1][1], wsol[-1][2]]

			#Update the values in the database
			self.set(LIT201, self.l[0])
			self.set(LIT202, self.l[1])
			self.set(LIT203, self.l[2])
			
			#logging.debug('Updating lit values in database:')
			logging.debug('lit201 is set to %s ', self.l[0])
			logging.debug('lit202 is set to %s ', self.l[1])
			logging.debug('lit203 is set to %s ', self.l[2])
			
			
			count += 1
			#self.lock = float(self.receive(LIT101, PLC_ADDR))
			time.sleep(PLC_PERIOD_SEC)

if __name__ == '__main__':
	plc201 = RawWaterTank(name='plant201',state=STATE,protocol=TANK_PROTOCOL2,memory=GENERIC_DATA,disk=GENERIC_DATA)
