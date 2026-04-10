# 📡 Broadcast Control using SDN (POX Controller)

## 📌 Project Overview

This project implements a Software Defined Networking (SDN) controller using POX to monitor and control broadcast traffic in a network.

Excessive broadcast packets can lead to network congestion and broadcast storms. This system limits broadcast traffic using a threshold-based approach.

---

## 🎯 Objectives

* Monitor broadcast packets in the network
* Control excessive broadcast traffic
* Prevent network congestion and broadcast storms

---

## 🛠️ Technologies Used

* Python
* POX Controller
* Mininet
* Linux (Ubuntu/WSL)

---

## ⚙️ How It Works

1. POX controller listens for incoming packets
2. Detects broadcast packets (FF:FF:FF:FF:FF:FF)
3. Counts packets per source MAC address
4. Allows packets up to a threshold
5. Blocks packets when threshold is exceeded

---

## 📊 Flow of Execution

Start → Packet Received → Check Broadcast → Count Packets →
If count ≤ Threshold → Allow
If count > Threshold → Block

---

## 📸 Results

* Normal communication works successfully
* Broadcast traffic is monitored
* Excessive broadcast packets are blocked

---

## 🚀 How to Run

### Step 1: Start POX Controller

```bash
cd ~/pox
./pox.py log.level --DEBUG broadcast_control
```

### Step 2: Run Mininet

```bash
sudo mn --topo single,4 --controller=remote
```

### Step 3: Test

```bash
pingall
h1 ping -b 10.0.0.255
```

---

## ✅ Output

* Broadcast allowed initially
* Blocked after threshold exceeded

---

## 🎓 Conclusion

This project demonstrates how SDN controllers can intelligently manage and restrict broadcast traffic to improve network performance.

---

## 👩‍💻 Authors

* KHUSHI GUPTA

---
