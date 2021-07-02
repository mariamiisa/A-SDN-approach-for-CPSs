"""
Store poth codes in the ~/pox/ext
./pox.py samples.pretty_log --DEBUG react-l2_learning react-flowremoved
"""
from pox.core import core
import pox.openflow.libopenflow_01 as of
import l2_learning as L2

log = core.getLogger()

def drop_dup (event):

  if event.idleTimeout is True:
    
    msg = of.ofp_flow_mod()
    log.debug("Installing the removed PLC flows")
    msg.match.dl_src = L2._handle_PacketIn.packet.dst
    msg.match.dl_dst = L2._handle_PacketIn.packet.src
    msg.idle_timeout = 5
    msg.flags = of.OFPFF_SEND_FLOW_REM
    msg.actions.append(of.ofp_action_enqueue(port = L2._handle_PacketIn.portevent, queue_id=1))
    event.connection.send(msg)
    
    # in the other direction
    msg = of.ofp_flow_mod()
    msg.match.dl_src = L2._handle_PacketIn.packet.src
    msg.match.dl_dst = L2._handle_PacketIn.packet.dst
    msg.idle_timeout = 5
    msg.data = L2._handle_PacketIn.dataaa
    msg.flags = of.OFPFF_SEND_FLOW_REM
    msg.actions.append(of.ofp_action_enqueue(port = L2._handle_PacketIn.porttable , queue_id=1))
    
    self.connection.send(msg)
    #log.debug("installing plc flow for %s.%i <-> %s.%i" %
    #(packet.src, event.port, packet.dst, port))
    

def launch ():
  # Listen to FlowRemoved events
  core.openflow.addListenerByName("FlowRemoved", drop_dup)
