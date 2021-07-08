from pox.lib.util import str_to_bool
import time
from utils import *
from pox.lib.addresses import EthAddr, IPAddr # Address types
from pox.core import core                     # Main POX object
import pox.openflow.libopenflow_01 as of      # OpenFlow 1.0 library
import pox.lib.packet as pkt                  # Packet parsing/construction
from pox.lib.addresses import EthAddr, IPAddr # Address types
import pox.lib.util as poxutil                # Various util functions
import pox.lib.revent as revent               # Event library
import pox.lib.recoco as recoco               # Multitasking library
from pox.lib.util import dpid_to_str, str_to_dpid



log = core.getLogger()
_flood_delay = 0

class LearningSwitch (object):

  def __init__ (self, connection, transparent):

    self.connection = connection
    self.transparent = transparent

    self.macToPort = {}

    connection.addListeners(self)
    
    self.hold_down_expired = _flood_delay == 0

  def _handle_FlowRemoved (self, event):
  
    if event.idleTimeout is True:
      
      if (_handle_PacketInDstPort == 8754 or _handle_PacketInDstPort == 7842 \
             or _handle_PacketInSrcPort == 8754 or _handle_PacketInSrcPort == 7842):   
    		
    		
    		#Rule between PLC and Q101
    		#S1
		    log.debug("FlowRemvedTriggered")
		    flowS1_1 = of.ofp_flow_mod()
		    flowS1_1.priority = 65535
		    flowS1_1.data = event.ofp
		    flowS1_1.match.dl_type = 0x800
		    flowS1_1.match.nw_dst = IPAddr("192.168.1.14")
		    flowS1_1.match.nw_src = IPAddr("192.168.1.11")
		    flowS1_1.actions.append(of.ofp_action_enqueue(port = 2, queue_id=1))
		    flowS1_1.actions.append(of.ofp_action_output(port = 2))
		    
        #S2
		    flowS2_1 = of.ofp_flow_mod()
		    flowS2_1.priority = 65535
		    flowS2_1.data = event.ofp
		    flowS2_1.match.dl_type = 0x800
		    flowS2_1.match.nw_dst = IPAddr("192.168.1.11")
		    flowS2_1.match.nw_src = IPAddr("192.168.1.14")
		    flowS2_1.actions.append(of.ofp_action_enqueue(port = 3, queue_id=1))
		    flowS2_1.actions.append(of.ofp_action_output(port = 3))
	    

        #Rule between PLC and Q102
        #S1
		    flowS1_2 = of.ofp_flow_mod()
		    flowS1_2.priority = 65535
		    flowS1_2.data = event.ofp
		    flowS1_2.match.dl_type = 0x800
		    flowS1_2.match.nw_dst = IPAddr("192.168.1.14")
		    flowS1_2.match.nw_src = IPAddr("192.168.1.12")
		    flowS1_2.actions.append(of.ofp_action_enqueue(port = 2, queue_id=1))
		    flowS1_2.actions.append(of.ofp_action_output(port = 2))
		    
		    
		    #S2
		    flowS2_2 = of.ofp_flow_mod()
		    flowS2_2.priority = 65535
		    flowS2_2.data = event.ofp
		    flowS2_2.match.dl_type = 0x800
		    flowS2_2.match.nw_dst = IPAddr("192.168.1.12")
		    flowS2_2.match.nw_src = IPAddr("192.168.1.14")
		    flowS2_2.actions.append(of.ofp_action_enqueue(port = 3, queue_id=1))
		    flowS2_2.actions.append(of.ofp_action_output(port = 3))		    
		    


        #Rule between PLC and LIT101
        #S1
		    flowS1_3 = of.ofp_flow_mod()
		    flowS1_3.priority = 65535
		    flowS1_3.data = event.ofp
		    flowS1_3.match.dl_type = 0x800
		    flowS1_3.match.nw_dst = IPAddr("192.168.1.14")
		    flowS1_3.match.nw_src = IPAddr("192.168.1.10")
		    flowS1_3.actions.append(of.ofp_action_enqueue(port = 2, queue_id=1))
		    flowS1_3.actions.append(of.ofp_action_output(port = 2))       
        
        
        
        #S2
		    flowS2_3 = of.ofp_flow_mod()
		    flowS2_3.priority = 65535
		    flowS2_3.data = event.ofp
		    flowS2_3.match.dl_type = 0x800
		    flowS2_3.match.nw_dst = IPAddr("192.168.1.10")
		    flowS2_3.match.nw_src = IPAddr("192.168.1.14")
		    flowS2_3.actions.append(of.ofp_action_enqueue(port = 3, queue_id=1))
		    flowS2_3.actions.append(of.ofp_action_output(port = 3))       
  
  
        #Rule between PLC and LIT102
        #S1
		    flowS1_4 = of.ofp_flow_mod()
		    flowS1_4.priority = 65535
		    flowS1_4.data = event.ofp
		    flowS1_4.match.dl_type = 0x800
		    flowS1_4.match.nw_dst = IPAddr("192.168.1.14")
		    flowS1_4.match.nw_src = IPAddr("192.168.1.18")
		    flowS1_4.actions.append(of.ofp_action_enqueue(port = 2, queue_id=1))
		    flowS1_4.actions.append(of.ofp_action_output(port = 2))       
         
        
        #S2
		    flowS2_4 = of.ofp_flow_mod()
		    flowS2_4.priority = 65535
		    flowS2_4.data = event.ofp
		    flowS2_4.match.dl_type = 0x800
		    flowS2_4.match.nw_dst = IPAddr("192.168.1.18")
		    flowS2_4.match.nw_src = IPAddr("192.168.1.14")
		    flowS2_4.actions.append(of.ofp_action_enqueue(port = 3, queue_id=1))
		    flowS2_4.actions.append(of.ofp_action_output(port = 3))
		    log.debug("Before if....")


        #MAYBE THERE's A PROBLEM HERE WITH self.connection
		    if dpid_to_str(self.connection.dpid) == "00-00-00-00-00-01":
		      self.connection.send(flowS1_1)
		      self.connection.send(flowS1_2)
		      self.connection.send(flowS1_3)
		      self.connection.send(flowS1_4)
		      log.debug("S1 flows are set...")
		  
		  
		    if dpid_to_str(self.connection.dpid) == "00-00-00-00-00-02":
		      self.connection.send(flowS2_1)
		      self.connection.send(flowS2_2)
		      self.connection.send(flowS2_3)
		      self.connection.send(flowS2_4)
		      log.debug("S2 flows are set...")		    
		    
		            

		    #log.debug("FlowTwo Done")
		    #log.debug("installing plc flow for second rule flowRemoved  %s.%i <-> %s.%i" %
                      #(_handle_PacketInpackeOneSrc,_handle_PacketInpacketPort , _handle_PacketInpackeOneDst , _handle_PacketInpackettwoPort))


  def _handle_PacketIn (self, event):

    packet = event.parsed
    tcpp = packet.find('tcp')

    
    
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
          
          global _handle_PacketInDstPort
          global _handle_PacketInSrcPort
          
          _handle_PacketInDstPort = dstp
          _handle_PacketInSrcPort = srcp
          
          if (dstp == 8754 or dstp == 7842 \
             or srcp == 8754 or srcp == 7842): 
            
              # install a flow rule in one direction    
              msg = of.ofp_flow_mod()
              log.debug("A PLC packet to port %s" % dstp)
              msg.priority = 1000
              msg.match.dl_dst = packet.src
              msg.match.dl_src = packet.dst
              log.debug("Setting idle timeout to 5")
              msg.idle_timeout = 5
              msg.flags = of.OFPFF_SEND_FLOW_REM
              msg.actions.append(of.ofp_action_output(port = event.port))
              event.connection.send(msg)
              
              global  _handle_PacketInpackeOneSrc 
              _handle_PacketInpackeOneSrc = packet.dst
              global _handle_PacketInpackeOneDst 
              _handle_PacketInpackeOneDst = packet.src
              global _handle_PacketInpacketPort 
              _handle_PacketInpacketPort = event.port

              # in the other direction
              msg = of.ofp_flow_mod()
              msg.priority = 1000
              msg.match.dl_src = packet.src
              msg.match.dl_dst = packet.dst
              msg.idle_timeout = 5
              msg.data = event.ofp
              msg.flags = of.OFPFF_SEND_FLOW_REM
              msg.actions.append(of.ofp_action_output(port = port))
              self.connection.send(msg)
              
              global _handle_PacketInpacketwoSrc 
              _handle_PacketInpacketwoSrc = packet.src
              global _handle_PacketInpacketwoDst
              _handle_PacketInpacketwoDst = packet.dst
              global _handle_PacketInpackettwoPort 
              _handle_PacketInpackettwoPort = port
              global _handle_PacketInpackettwodata
              _handle_PacketInpackettwodata = msg.data

              log.debug("installing plc flow for second rule packet in %s.%i <-> %s.%i" %
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
    #log.debug("Connection ID: ", (event.connection.dpid,))
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
