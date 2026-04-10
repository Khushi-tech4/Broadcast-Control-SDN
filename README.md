📡 Broadcast Control using SDN (POX Controller)
📌 Problem Statement

In Software Defined Networking (SDN), excessive broadcast traffic can lead to network congestion and broadcast storms, which degrade overall network performance.
This project implements a POX-based SDN controller that monitors broadcast packets and restricts them using a threshold-based control mechanism to ensure efficient network operation and prevent flooding.

🎯 Objectives
Monitor broadcast packets in the network
Detect excessive broadcast traffic
Limit broadcast packets using a predefined threshold
Prevent network congestion and broadcast storms
Improve overall network efficiency using SDN control logic
🛠️ Technologies Used
Python
POX SDN Controller
Mininet Network Emulator
Linux (Ubuntu / WSL)
⚙️ Conditions to be Satisfied (Core Logic)

The controller enforces the following conditions:

Packet must be a broadcast packet (FF:FF:FF:FF:FF:FF)
Source MAC address is tracked individually
A counter is maintained per source
If broadcast count ≤ threshold → Allow packet
If broadcast count > threshold → Block packet
Decision is made in real-time by the POX controller
🔄 Flow of Execution

Start Network
→ Packet Received by Switch
→ Sent to POX Controller
→ Check if Broadcast Packet
→ Identify Source MAC
→ Increment Counter
→ Compare with Threshold
  ├── If within limit → Forward Packet
  └── If exceeded → Drop Packet

🧰 Setup & Execution Steps
Step 1: Install Requirements

Make sure you have:

Mininet
POX Controller
Python 2.7 (recommended for POX)
Step 2: Start POX Controller
cd ~/pox
./pox.py log.level --DEBUG broadcast_control
Step 3: Run Mininet Topology
sudo mn --topo single,4 --controller=remote
Step 4: Test Broadcast Control

Inside Mininet CLI:

pingall
h1 ping -b 10.0.0.255
📊 Expected Output
✅ Normal Scenario
Initial broadcast packets are allowed
Hosts communicate successfully
Controller logs packet flow
⚠️ After Threshold Exceeded
Broadcast packets from same source are blocked
Controller drops excessive packets
Network congestion is reduced
📸 Result Summary
Broadcast traffic is successfully monitored
Threshold-based filtering is applied
Network remains stable under broadcast load
Demonstrates SDN-based intelligent traffic control
🎓 Conclusion

This project demonstrates how SDN controllers like POX can be used to intelligently manage network traffic. By applying a threshold-based broadcast control mechanism, the system effectively prevents broadcast storms and improves overall network performance.

👩‍💻 Authors
Khushi Gupta
