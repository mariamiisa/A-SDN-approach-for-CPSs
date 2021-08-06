"""
simple-cps run.py
"""

from mininet.net import Mininet
from mininet.cli import CLI
from mininet.node import Controller, RemoteController, CPULimitedHost

from minicps.mcps import MiniCPS

from topo import DumbbellTopo

import sys

import time

import subprocess

import logging

from utils1 import IP

from mininet.link import Intf, TCLink

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
        
        lit201 = self.net.get('lit201')
        lit201.cmd('python lit201.py &')
        
        lit202 = self.net.get('lit202')
        lit202.cmd('python lit202.py &')
        
        q201 = self.net.get('q201')
        q201.cmd('python q201.py &')
        
        q202 = self.net.get('q202')
        q202.cmd('python q202.py &')
        
        
        
        # start devices
        CLI(self.net)

        self.net.stop()

if __name__ == "__main__":

    #topo = SimpleTopo()
    topo = DumbbellTopo()
    #controller = RemoteController('c0', ip=IP['controller'], port=6633 )
    controller = RemoteController('c0', ip=IP['controller'], port=6633 )
    net = Mininet(topo=topo, controller = controller, host=CPULimitedHost, link= TCLink)

    dynamic_cps = SimpleCPS(name='industry', net=net)
