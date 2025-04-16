# pysniff.py
import scapy.all as scapy
import argparse
from datetime import datetime

# Function to capture packets
def packet_callback(packet):
    print(f"Timestamp: {datetime.now()}")
    print(f"Packet Summary: {packet.summary()}")

    # Check if the packet has an IP layer and is an IPv4 packet
    if packet.haslayer(scapy.IP):
        ip_src = packet[scapy.IP].src
        ip_dst = packet[scapy.IP].dst
        print(f"Source IP: {ip_src} -> Destination IP: {ip_dst}")

        # Check if packet has a TCP layer
        if packet.haslayer(scapy.TCP):
            print(f"TCP Layer: Source Port: {packet[scapy.TCP].sport} -> Destination Port: {packet[scapy.TCP].dport}")

        # Check if packet has a UDP layer
        if packet.haslayer(scapy.UDP):
            print(f"UDP Layer: Source Port: {packet[scapy.UDP].sport} -> Destination Port: {packet[scapy.UDP].dport}")

    print("-" * 50)

# Function to start sniffing
def start_sniffing(interface):
    print(f"Starting packet sniffing on interface: {interface}...")
    scapy.sniff(iface=interface, prn=packet_callback, store=0)  # store=0 ensures we don't keep the packets in memory

# Function to handle arguments
def parse_arguments():
    parser = argparse.ArgumentParser(description="PySniff - Network Sniffer and Packet Analyzer")
    parser.add_argument("-i", "--interface", type=str, required=True, help="The network interface to sniff on")
    return parser.parse_args()

# Main function
if __name__ == "__main__":
    args = parse_arguments()
    start_sniffing(args.interface)
