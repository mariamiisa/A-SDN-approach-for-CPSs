"""
Dumbbell Topology
"""

from mininet.node import Host, Node
from mininet.topo import Topo
from utils import IP, NETMASK
from utils1 import IP, NETMASK
from mininet.link import TCLink


class LinuxRouter( Node ):
	"A Node with IP forwarding enabled."

	def config( self, **params ):
		super( LinuxRouter, self).config( **params )
		# Enable forwarding on the router
		self.cmd( 'sysctl net.ipv4.ip_forward=1' )

	def terminate( self ):
		self.cmd( 'sysctl net.ipv4.ip_forward=0' )
		super( LinuxRouter, self ).terminate()




class DumbbellTopo(Topo):

	"""
	Dumbbell topology: 
	plant 	   <--> S1 <--> S2 <-->  PLC
	udpclient 			  udpserver
	"""
	
	def build(self):
	

		# Add router
		defaultIP = IP['plc101']+NETMASK
		
		
		# Add Switches
		S1 = self.addSwitch('S1')
		S2 = self.addSwitch('S2')

		gateway = 'via ' + defaultIP
		
		
		# Add nodes for first plc 1
		PLC101 = self.addNode('plc101', ip=IP['plc101'] + NETMASK, cls=LinuxRouter)
		
		q101= self.addHost('q101', ip=IP['q101'] + NETMASK, defaultRoute=gateway)
		q102= self.addHost('q102',ip=IP['q102'] + NETMASK, defaultRoute=gateway)
		
		lit101= self.addHost('lit101',ip=IP['lit101'] + NETMASK, defaultRoute=gateway)
		lit102= self.addHost('lit102',ip=IP['lit102'] + NETMASK, defaultRoute=gateway)
		lit103= self.addHost('lit103',ip=IP['lit103'] + NETMASK, defaultRoute=gateway)
		
		plant101 = self.addHost('plant101',ip=IP['plant101'] + NETMASK, defaultRoute=gateway)
		
		client = self.addHost('client', ip=IP['client'] + NETMASK, defaultRoute=gateway)
		server = self.addHost('server', ip=IP['server'] + NETMASK, defaultRoute=gateway)
		
		
		# Add nodes for first plc 2
		PLC201 = self.addNode('plc201', ip = IP['plc201'] + NETMASK, cls=LinuxRouter)

		q201= self.addHost('q201', ip=IP['q201'] + NETMASK, defaultRoute=gateway)
		q202= self.addHost('q202',ip=IP['q202'] + NETMASK, defaultRoute=gateway)	
		
		plant201 = self.addHost('plant201',ip=IP['plant201'] + NETMASK, defaultRoute=gateway)	

		lit201= self.addHost('lit201',ip=IP['lit201'] + NETMASK, defaultRoute=gateway)
		lit202= self.addHost('lit202',ip=IP['lit202'] + NETMASK, defaultRoute=gateway)
		lit203= self.addHost('lit203',ip=IP['lit203'] + NETMASK, defaultRoute=gateway)		

		# Add links
		
		self.addLink( S2, PLC201, intfName2='plc1-eth1', params2={'ip' : defaultIP} ,cls=TCLink , delay='1ms' ,bw=100)
		self.addLink( S2, PLC101, intfName2='plc1-eth1', params2={'ip' : defaultIP} ,cls=TCLink , delay='1ms' ,bw=100)
		
		self.addLink(S2,server ,cls=TCLink , delay='1ms' ,bw=100)
		self.addLink(S1,client ,cls=TCLink , delay='1ms' ,bw=100)
		
		self.addLink(S1,S2 ,cls=TCLink , delay='10ms' ,bw=1)

		
		self.addLink(q101, S1 ,cls=TCLink , delay='1ms' ,bw=100)
		self.addLink(q102, S1 ,cls=TCLink , delay='1ms' ,bw=100)
		
		self.addLink(q201, S1 ,cls=TCLink , delay='1ms' ,bw=100)
		self.addLink(q202, S1 ,cls=TCLink , delay='1ms' ,bw=100)
		
		self.addLink(plant101, S1 ,cls=TCLink , delay='1ms' ,bw=100)	
				
		self.addLink(lit101, S1 ,cls=TCLink , delay='1ms' ,bw=100)
		self.addLink(lit102, S1 ,cls=TCLink , delay='1ms' ,bw=100)
		self.addLink(lit103, S1 ,cls=TCLink , delay='1ms' ,bw=100)
		
		self.addLink(plant201, S1 ,cls=TCLink , delay='1ms' ,bw=100)	
				
		self.addLink(lit201, S1 ,cls=TCLink , delay='1ms' ,bw=100)
		self.addLink(lit202, S1 ,cls=TCLink , delay='1ms' ,bw=100)
		self.addLink(lit203, S1 ,cls=TCLink , delay='1ms' ,bw=100)

