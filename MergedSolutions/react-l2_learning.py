from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.util import dpid_to_str, str_to_dpid
from pox.lib.util import str_to_bool
import time

log = core.getLogger()
_flood_delay = 0

class LearningSwitch (object):

  def __init__ (self, connection, transparent):

    self.connection = connection
    self.transparent = transparent

    self.macToPort = {}

    connection.addListeners(self)
    
    self.hold_down_expired = _flood_delay == 0


  def _handle_PacketIn (self, event):

    _handle_PacketIn.packet = event.parsed
    tcpp = packet.find('tcp')
    
    _handle_PacketIn.dataaa= event.data
    _handle_PacketIn.portevent = event.port
    
    
    def flood (message = None):
      """ Floods the packet """
      msg = of.ofp_packet_out()
      if time.time() - self.connection.connect_time >= _flood_delay:

        if self.hold_down_expired is False:
          self.hold_down_expired = True
          log.info("%s: Flood hold-down expired -- flooding",
              dpid_to_str(event.dpid))

        if message is not None: log.debug(message)

        msg.actions.append(of.ofp_action_output(port = of.OFPP_FLOOD))
      else:
        pass

      msg.data = event.ofp
      msg.in_port = event.port
      self.connection.send(msg)

      
      
    def drop (duration = None):
      """
      Drops this packet and optionally installs a flow to continue
      dropping similar ones for a while
      """
      if duration is not None:
        if not isinstance(duration, tuple):
          duration = (duration,duration)
        msg = of.ofp_flow_mod()
        msg.match = of.ofp_match.from_packet(packet)
        msg.idle_timeout = duration[0]
        msg.hard_timeout = duration[1]
        msg.buffer_id = event.ofp.buffer_id
        self.connection.send(msg)
      elif event.ofp.buffer_id is not None:
        msg = of.ofp_packet_out()
        msg.buffer_id = event.ofp.buffer_id
        msg.in_port = event.port
        self.connection.send(msg)

        
        
    self.macToPort[packet.src] = event.port # 1

    
    if not self.transparent: # 2
      if packet.type == packet.LLDP_TYPE or packet.dst.isBridgeFiltered():
        drop() # 2a
        return

    if packet.dst.is_multicast:
      flood() # 3a
    else:
      if packet.dst not in self.macToPort: # 4
        flood("Port for %s unknown -- flooding" % (packet.dst,)) # 4a
      else:
        port = self.macToPort[packet.dst]
        _handle_PacketIn.porttable = port

        
        if port == event.port: # 5
          # 5a
          log.warning("Same port for packet from %s -> %s on %s.%s.  Drop."
              % (packet.src, packet.dst, dpid_to_str(event.dpid), port))
          drop(10)
          return
        # 6
             
        if tcpp is not None:
          dstp = tcpp.dstport
          srcp = tcpp.srcport
          
          if (dstp == 8754 or dstp == 7842 \
             or srcp == 8754 or srcp == 7842): 
            
              # install a flow rule in one direction    
              msg = of.ofp_flow_mod()
              log.debug("A PLC packet to port %s" % dstp)
              msg.match.dl_dst = packet.src
              msg.match.dl_src = packet.dst
              log.debug("Setting idle timeout to 5")
              msg.idle_timeout = 5
              msg.flags = of.OFPFF_SEND_FLOW_REM
              msg.actions.append(of.ofp_action_output(port = event.port))
              event.connection.send(msg)
              
              # in the other direction
              msg = of.ofp_flow_mod()
              msg.match.dl_src = packet.src
              msg.match.dl_dst = packet.dst
              msg.idle_timeout = 5
              msg.data = event.ofp
              msg.flags = of.OFPFF_SEND_FLOW_REM
              msg.actions.append(of.ofp_action_output(port = port))
              self.connection.send(msg)
              log.debug("installing plc flow for %s.%i <-> %s.%i" %
                  (packet.src, event.port, packet.dst, port))

          else:
              log.debug("installing flow for %s.%i -> %s.%i" %
                  (packet.src, event.port, packet.dst, port))
              msg = of.ofp_flow_mod()
              msg.match = of.ofp_match.from_packet(packet, event.port)
              msg.idle_timeout = 20
              msg.hard_timeout = 40
              msg.actions.append(of.ofp_action_output(port = port))
              msg.data = event.ofp # 6a
              self.connection.send(msg)


        else:
          log.debug("installing flow for %s.%i -> %s.%i" %
                  (packet.src, event.port, packet.dst, port))
          msg = of.ofp_flow_mod()
          msg.match = of.ofp_match.from_packet(packet, event.port)
          msg.idle_timeout = 20
          msg.hard_timeout = 40
          msg.actions.append(of.ofp_action_output(port = port))
          msg.data = event.ofp # 6a
          self.connection.send(msg)


class l2_learning (object):
  """
  Waits for OpenFlow switches to connect and makes them learning switches.
  """
  def __init__ (self, transparent, ignore = None):
    """
    Initialize

    See LearningSwitch for meaning of 'transparent'
    'ignore' is an optional list/set of DPIDs to ignore
    """
    core.openflow.addListeners(self)
    self.transparent = transparent
    self.ignore = set(ignore) if ignore else ()

  def _handle_ConnectionUp (self, event):
    if event.dpid in self.ignore:
      log.debug("Ignoring connection %s" % (event.connection,))
      return
    log.debug("Connection %s" % (event.connection,))
    LearningSwitch(event.connection, self.transparent)


def launch (transparent=False, hold_down=_flood_delay, ignore = None):
  """
  Starts an L2 learning switch.
  """
  try:
    global _flood_delay
    _flood_delay = int(str(hold_down), 10)
    assert _flood_delay >= 0
  except:
    raise RuntimeError("Expected hold-down to be a number")

  if ignore:
    ignore = ignore.replace(',', ' ').split()
    ignore = set(str_to_dpid(dpid) for dpid in ignore)

  core.registerNew(l2_learning, str_to_bool(transparent), ignore)
