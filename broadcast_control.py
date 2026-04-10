from pox.core import core
import pox.openflow.libopenflow_01 as of

log = core.getLogger()

# ---------------------------------------------------
# BROADCAST CONTROL SDN CONTROLLER
# ---------------------------------------------------
# This controller prevents broadcast storms by:
# 1. Tracking broadcast packets per source MAC
# 2. Allowing only limited broadcasts (threshold)
# 3. Blocking excess broadcast traffic
# ---------------------------------------------------

broadcast_count = {}
THRESHOLD = 10


def _handle_PacketIn(event):
    """
    Handles packets arriving at the switch.
    This is the core of reactive SDN behavior.
    """

    packet = event.parsed
    src = str(packet.src)
    dst = str(packet.dst)

    # ---------------------------------------------------
    # CHECK FOR BROADCAST PACKET
    # ---------------------------------------------------
    if dst == "ff:ff:ff:ff:ff:ff":

        # Increase broadcast count per host
        broadcast_count[src] = broadcast_count.get(src, 0) + 1
        count = broadcast_count[src]

        log.info("[BROADCAST] Source: %s | Count: %d", src, count)

        # ---------------------------------------------------
        # BLOCK IF THRESHOLD EXCEEDED
        # ---------------------------------------------------
        if count > THRESHOLD:
            log.warning("🚫 BLOCKED Broadcast from %s (Limit Exceeded)", src)
            return  # Drop packet

        else:
            log.info("✅ ALLOWED Broadcast from %s", src)

    # ---------------------------------------------------
    # FORWARD PACKET (FLOOD)
    # ---------------------------------------------------
    msg = of.ofp_packet_out()
    msg.data = event.ofp
    msg.actions.append(of.ofp_action_output(port=of.OFPP_FLOOD))
    event.connection.send(msg)


def launch():
    """
    Initializes the POX controller module
    """
    log.info("🚀 Broadcast Control SDN Controller Started")
    core.openflow.addListenerByName("PacketIn", _handle_PacketIn)
