"""
Store poth codes in the ~/pox/ext
./pox.py samples.pretty_log --DEBUG l2_learning flowremoved
"""
from pox.core import core
import pox.openflow.libopenflow_01 as of

log = core.getLogger()

def drop_dup (event):

  if event.idleTimeout is True:
    log.debug("Dropping udp packets")
    msg = of.ofp_flow_mod()
    msg.priority = 65535
    msg.match.dl_type = 0x800
    msg.match.nw_proto = 17
    event.connection.send(msg)

def launch ():
  # Listen to FlowRemoved events
  core.openflow.addListenerByName("FlowRemoved", drop_dup)
