"""
Dumbbell Topology
"""

from mininet.node import Host, Node
from mininet.topo import Topo
from utils import IP, NETMASK
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
	plant  <--> Switch1 <--> Switch2 <-->  PLC
	client 			                           server
	"""
	
	def build(self):
	

		# Add router
		defaultIP = IP['plc101']+NETMASK
		
		
		# Add Switches
		S1 = self.addSwitch('S1')
		S2 = self.addSwitch('S2')

		gateway = 'via ' + defaultIP
    
		
		# Add nodes
		PLC101 = self.addNode('plc101', ip=IP['plc101'] + NETMASK, cls=LinuxRouter)
		
		q101= self.addHost('q101', ip=IP['q101'] + NETMASK, defaultRoute=gateway)
		q102= self.addHost('q102',ip=IP['q102'] + NETMASK, defaultRoute=gateway)
		
		lit101= self.addHost('lit101',ip=IP['lit101'] + NETMASK, defaultRoute=gateway)
		lit102= self.addHost('lit102',ip=IP['lit102'] + NETMASK, defaultRoute=gateway)
		lit103= self.addHost('lit103',ip=IP['lit103'] + NETMASK, defaultRoute=gateway)
		
		plant101 = self.addHost('plant101',ip=IP['plant101'] + NETMASK, defaultRoute=gateway)
    
    client = self.addHost('client', ip=IP['client'] + NETMASK, defaultRoute=gateway) 
    server = self.addHost('server', ip=IP['server'] + NETMASK, defaultRoute=gateway)
		

		# Add links

		self.addLink( S2, PLC101, intfName2='plc1-eth1', params2={ 'ip' : defaultIP } ,cls=TCLink , delay='1ms' ,bw=100)
    
    self.addLink(S2,server ,cls=TCLink , delay='1ms' ,bw=100)
    self.addLink(S1,client ,cls=TCLink , delay='1ms' ,bw=100)
		
		self.addLink(S1,S2 ,cls=TCLink , delay='10ms' ,bw=1)
		
		self.addLink(q101, S1 ,cls=TCLink , delay='1ms' ,bw=100)
		self.addLink(q102, S1 ,cls=TCLink , delay='1ms' ,bw=100)
		
		self.addLink(plant101, S1 ,cls=TCLink , delay='1ms' ,bw=100)	
				
		self.addLink(lit101, S1 ,cls=TCLink , delay='1ms' ,bw=100)
		self.addLink(lit102, S1 ,cls=TCLink , delay='1ms' ,bw=100)
		self.addLink(lit103, S1 ,cls=TCLink , delay='1ms' ,bw=100)

