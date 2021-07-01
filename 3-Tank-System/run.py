"""
simple-cps run.py
"""

from mininet.net import Mininet
from mininet.cli import CLI
from mininet.node import Controller, RemoteController, CPULimitedHost
from mininet.link import Intf, TCLink

from minicps.mcps import MiniCPS
from topo import DumbbellTopo

import sys
import time
import subprocess
import logging

from utils import IP

class SimpleCPS(MiniCPS):

    """Main container used to run the simulation."""

    def __init__(self, name, net):

        self.name = name
        self.net = net

        self.net.start()

        lit101 = self.net.get('lit101')
        lit101.cmd('rm -rf lit101.log')
        lit101.cmd('python lit101.py &')

        #lit103 = self.net.get('lit103')
        #lit103.cmd('rm -rf lit103.log')
        #lit103.cmd('python lit103.py &')

        lit102 = self.net.get('lit102')
        lit102.cmd('rm -rf lit102.log')
        lit102.cmd('python lit102.py &')
        
        q101 = self.net.get('q101')
        q101.cmd('rm -rf q1.log')
        q101.cmd('python q101.py &')

        q102 = self.net.get('q102')
        q101.cmd('rm -rf q2.log')
        q102.cmd('python q102.py &')
        
        plc101 = self.net.get('plc101')
        plc101.cmd('rm -rf plc.log')        

        plant101 = self.net.get('plant101')
        plant101.cmd('rm -rf plant.log')
        
        # start devices
        CLI(self.net)
        self.net.stop()

if __name__ == "__main__":

    topo = DumbbellTopo()
    controller = RemoteController('c0', ip=IP['controller'], port=6633 )
    net = Mininet(topo=topo, controller = controller, host=CPULimitedHost, link= TCLink)
    dynamic_cps = SimpleCPS(name='industry', net=net)
