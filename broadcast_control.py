from pox.core import core
import pox.openflow.libopenflow_01 as of

log = core.getLogger()

broadcast_count = {}
THRESHOLD = 10

def _handle_PacketIn(event):
    packet = event.parsed
    src = str(packet.src)
    dst = str(packet.dst)

    # Check if broadcast
    if dst == "ff:ff:ff:ff:ff:ff":
        broadcast_count[src] = broadcast_count.get(src, 0) + 1
        count = broadcast_count[src]

        log.info("[Broadcast] Src: %s | Count: %d", src, count)

        if count > THRESHOLD:
            log.warning("🚫 BLOCKED Broadcast from %s (Limit Exceeded)", src)
            return  # Drop packet

        else:
            log.info("✅ Allowing Broadcast from %s", src)

    # Forward packet
    msg = of.ofp_packet_out()
    msg.data = event.ofp
    msg.actions.append(of.ofp_action_output(port=of.OFPP_FLOOD))
    event.connection.send(msg)


def launch():
    log.info("🚀 Initializing Broadcast Control Module")
    core.openflow.addListenerByName("PacketIn", _handle_PacketIn)
