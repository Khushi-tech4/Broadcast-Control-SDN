🚀 Broadcast Traffic Control using SDN (Ryu + Mininet)
👤 Author

Name:Khushi Gupta
Course: BTech CSE( AI&ML)
Project Type: Individual SDN Mininet Project

📌 Problem Statement

In traditional networks, broadcast traffic (such as ARP requests) can lead to broadcast storms, causing network congestion and performance degradation.

This project implements a Software Defined Networking (SDN) based solution using a Ryu controller to detect, control, and limit excessive broadcast traffic by dynamically installing OpenFlow rules in the switch.

🎯 Objectives
Detect broadcast packets in the network
Allow limited broadcast traffic for normal operation
Block excessive broadcast traffic after a defined threshold
Install dynamic flow rules using OpenFlow
Observe network performance improvement
🛠️ Technologies Used
Mininet (Network Emulator)
Ryu SDN Controller
OpenFlow 1.3
iperf (Throughput testing)
ping (Latency testing)
Wireshark (Optional analysis tool)
🖧 Network Topology

Single switch topology with 3 hosts:

h1 --- s1 --- h2
     |
     h3

⚙️ Setup Instructions

Step 1: Clean Mininet
sudo mn -c

Step 2: Run Ryu Controller
ryu-manager broadcast_control.py

Step 3: Start Mininet
sudo mn --topo single,3 --controller remote

▶️ Execution Steps

Generate broadcast traffic (ARP flood simulation):
h1 arping -c 20 10.0.0.99

Check connectivity:
pingall

Measure throughput:
iperf h1 h2

🎯 Expected Output

Controller logs:
[ALLOWED] Broadcast Packet #1
[ALLOWED] Broadcast Packet #2
[ALLOWED] Broadcast Packet #3
[ALLOWED] Broadcast Packet #4
[ALLOWED] Broadcast Packet #5
[BLOCKED] Broadcast Packet #6
🚫 INSTALLING DROP RULE 🚫

This shows that initial broadcast packets are allowed, and after reaching threshold, broadcast traffic is blocked using a flow rule.

📊 Flow Table Verification

Command:
sudo ovs-ofctl -O OpenFlow13 dump-flows s1

Expected output includes:
priority=100,dl_dst=ff:ff:ff:ff:ff:ff actions=drop

This confirms that broadcast packets are being dropped at the switch level using OpenFlow rules.

📈 Performance Analysis
Ping (Latency Test)

h1 ping h2

Used to measure delay between hosts and verify connectivity.

iperf (Throughput Test)

iperf h1 h2

Example output:
33.4 Gbits/sec

This high value is expected because Mininet runs in a virtual environment without real hardware constraints.

🔍 Observations
Broadcast packets are initially forwarded to the controller
After threshold, a high-priority drop rule is installed
Switch blocks broadcast traffic directly
Network load is reduced after control implementation
📸 Proof of Execution

Screenshots included in GitHub repository:

Controller logs showing allowed and blocked packets
Flow table showing DROP rule
Mininet execution (arping / ping / iperf)
Performance results
🧠 SDN Concepts Demonstrated
Controller–Switch communication
Packet-in event handling
Match–Action flow rules
Dynamic flow rule installation
Traffic monitoring and control
✅ Conclusion

This project demonstrates how SDN can effectively control broadcast traffic by dynamically installing OpenFlow rules. It improves network efficiency by reducing unnecessary broadcast flooding and optimizing traffic flow.

📚 References
Ryu SDN Framework Documentation
Mininet Official Documentation
OpenFlow Switch Specification 
PROOF OF EXECUTION:<img width="786" height="430" alt="Screenshot from 2026-04-20 11-12-17" src="https://github.com/user-attachments/assets/d6f28e9e-b884-4ffe-b7d1-056e81aae4f7" />
<img width="1210" height="773" alt="Screenshot from 2026-04-20 11-12-57" src="https://github.com/user-attachments/assets/c54f23b6-d072-47da-a9f0-838f015c2d55" />

<img width="1210" height="773" alt="Screenshot from 2026-04-20 11-13-28" src="https://github.com/user-attachments/assets/01e70682-7d88-4b24-840c-77841096e894" />
