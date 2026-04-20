# ==========================================================
# Broadcast Traffic Control using SDN (Ryu Controller)
# ==========================================================
# Features:
# - Detect broadcast packets (ARP / FF:FF:FF:FF:FF:FF)
# - Allow limited broadcast traffic (normal behavior)
# - Block excessive broadcast traffic dynamically
# - Install OpenFlow flow rules in switch
# - Demonstrate SDN controller-switch interaction
# ==========================================================

from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER, set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet, ethernet


class BroadcastControl(app_manager.RyuApp):
    """
    Main SDN Controller Application
    Inherits from RyuApp to handle OpenFlow events
    """

    # Use OpenFlow 1.3 protocol
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(BroadcastControl, self).__init__(*args, **kwargs)

        # MAC learning table: {switch_id: {mac: port}}
        self.mac_to_port = {}

        # Counter for broadcast packets per switch
        self.broadcast_count = {}

        # Flag to ensure blocking happens only once
        self.blocked = False

    # ==========================================================
    # SWITCH SETUP FUNCTION
    # Called when switch connects to controller
    # ==========================================================
    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):

        datapath = ev.msg.datapath
        parser = datapath.ofproto_parser
        ofproto = datapath.ofproto

        # ------------------------------------------------------
        # RULE 1: Send ALL broadcast packets to controller
        # This ensures controller can monitor broadcast traffic
        # ------------------------------------------------------
        match = parser.OFPMatch(eth_dst="ff:ff:ff:ff:ff:ff")
        actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER)]
        self.add_flow(datapath, 50, match, actions)

        # ------------------------------------------------------
        # RULE 2: Default rule (unknown packets → controller)
        # ------------------------------------------------------
        match = parser.OFPMatch()
        actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER)]
        self.add_flow(datapath, 0, match, actions)

    # ==========================================================
    # FUNCTION TO INSTALL FLOW RULES INTO SWITCH
    # ==========================================================
    def add_flow(self, datapath, priority, match, actions, idle_timeout=0):

        parser = datapath.ofproto_parser
        ofproto = datapath.ofproto

        # Define instruction set (what action to apply)
        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS, actions)]

        # Create flow mod message
        mod = parser.OFPFlowMod(
            datapath=datapath,
            priority=priority,
            match=match,
            instructions=inst,
            idle_timeout=idle_timeout
        )

        # Send flow rule to switch
        datapath.send_msg(mod)

    # ==========================================================
    # PACKET-IN HANDLER
    # Triggered when switch sends packet to controller
    # ==========================================================
    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def packet_in_handler(self, ev):

        msg = ev.msg
        datapath = msg.datapath
        parser = datapath.ofproto_parser
        ofproto = datapath.ofproto

        # Parse incoming packet
        pkt = packet.Packet(msg.data)
        eth = pkt.get_protocol(ethernet.ethernet)

        dst = eth.dst
        src = eth.src

        dpid = datapath.id  # Switch ID
        in_port = msg.match['in_port']

        # Initialize MAC table for switch
        self.mac_to_port.setdefault(dpid, {})

        # Learn MAC address → port mapping
        self.mac_to_port[dpid][src] = in_port

        # ======================================================
        # BROADCAST TRAFFIC DETECTION
        # ======================================================
        if dst == "ff:ff:ff:ff:ff:ff":

            # Count broadcast packets
            self.broadcast_count[dpid] = self.broadcast_count.get(dpid, 0) + 1
            count = self.broadcast_count[dpid]

            # --------------------------------------------------
            # ALLOW first 5 broadcast packets
            # --------------------------------------------------
            if count <= 5:
                print(f"[ALLOWED] Broadcast Packet #{count}")

            # --------------------------------------------------
            # BLOCK broadcast traffic after threshold
            # --------------------------------------------------
            elif count == 6 and not self.blocked:

                print(f"[BLOCKED] Broadcast Packet #{count}")
                print("\n🚫 INSTALLING DROP RULE 🚫\n")

                # Create match rule for broadcast MAC
                match = parser.OFPMatch(eth_dst="ff:ff:ff:ff:ff:ff")

                # DROP action (empty action list = drop packet)
                actions = []

                # Install high priority flow rule in switch
                self.add_flow(datapath, 100, match, actions)

                # Set flag so blocking happens only once
                self.blocked = True

        # ======================================================
        # LEARNING SWITCH LOGIC (NORMAL FORWARDING)
        # ======================================================

        # If destination MAC is known → forward normally
        if dst in self.mac_to_port[dpid]:
            out_port = self.mac_to_port[dpid][dst]

        # If unknown → flood
        else:
            out_port = ofproto.OFPP_FLOOD

        actions = [parser.OFPActionOutput(out_port)]

        # Install forwarding rule in switch
        match = parser.OFPMatch(in_port=in_port, eth_dst=dst)

        self.add_flow(datapath, 10, match, actions, idle_timeout=30)

        # Send packet out through switch
        out = parser.OFPPacketOut(
            datapath=datapath,
            buffer_id=msg.buffer_id,
            in_port=in_port,
            actions=actions,
            data=msg.data
        )

        datapath.send_msg(out)
