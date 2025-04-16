# pysniff_gui_enhanced.py
import scapy.all as scapy
from scapy.arch.windows import get_windows_if_list  # ✅ Proper import for Windows interfaces
import threading
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
from datetime import datetime


captured_packets = []
stop_sniffing = False
dark_mode = False
interface_map = {}  # Maps friendly name -> NPF name

def packet_callback(packet):
    global captured_packets

    if stop_sniffing:
        return False

    # Filtering by IP and Protocol
    filter_ip = ip_filter_var.get().strip()
    filter_proto = proto_filter_var.get().lower()

    if filter_ip and not (packet.haslayer(scapy.IP) and (packet[scapy.IP].src == filter_ip or packet[scapy.IP].dst == filter_ip)):
        return

    if filter_proto and filter_proto != "all":
        if filter_proto == "tcp" and not packet.haslayer(scapy.TCP):
            return
        elif filter_proto == "udp" and not packet.haslayer(scapy.UDP):
            return
        elif filter_proto == "icmp" and not packet.haslayer(scapy.ICMP):
            return

    captured_packets.append(packet)

    output = f"\n[{datetime.now().strftime('%H:%M:%S')}]\n"
    output += f"Packet Summary: {packet.summary()}\n"

    if packet.haslayer(scapy.IP):
        ip_src = packet[scapy.IP].src
        ip_dst = packet[scapy.IP].dst
        output += f"IP: {ip_src} ➝ {ip_dst}\n"

        if packet.haslayer(scapy.TCP):
            output += f"TCP: {packet[scapy.TCP].sport} ➝ {packet[scapy.TCP].dport}\n"
        if packet.haslayer(scapy.UDP):
            output += f"UDP: {packet[scapy.UDP].sport} ➝ {packet[scapy.UDP].dport}\n"

    output += "-" * 60 + "\n"
    gui_output.insert(tk.END, output)
    gui_output.see(tk.END)

def start_sniff_thread(interface):
    global stop_sniffing, captured_packets
    stop_sniffing = False
    captured_packets = []
    try:
        scapy.sniff(iface=interface, prn=packet_callback, store=0)
    except Exception as e:
        messagebox.showerror("Error", str(e))

def start_sniffing():
    friendly_name = interface_var.get()
    if not friendly_name:
        messagebox.showwarning("Warning", "Please select a network interface.")
        return

    npf_device = interface_map.get(friendly_name)
    if not npf_device:
        messagebox.showerror("Error", "Selected interface not found.")
        return

    gui_output.insert(tk.END, f"\n[+] Sniffing started on {friendly_name}\n" + "-"*60 + "\n")
    threading.Thread(target=start_sniff_thread, args=(npf_device,), daemon=True).start()

def stop_sniff():
    global stop_sniffing
    stop_sniffing = True
    gui_output.insert(tk.END, "\n[-] Sniffing stopped.\n" + "-"*60 + "\n")

def export_to_txt():
    if not captured_packets:
        messagebox.showinfo("Info", "No packets to export.")
        return

    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
    if file_path:
        with open(file_path, "w") as f:
            for pkt in captured_packets:
                f.write(pkt.summary() + "\n")
        messagebox.showinfo("Success", f"Packets exported to {file_path}")

def export_to_pcap():
    if not captured_packets:
        messagebox.showinfo("Info", "No packets to export.")
        return

    file_path = filedialog.asksaveasfilename(defaultextension=".pcap", filetypes=[("PCAP Files", "*.pcap")])
    if file_path:
        scapy.wrpcap(file_path, captured_packets)
        messagebox.showinfo("Success", f"Packets saved to {file_path}")

def clear_output():
    gui_output.delete(1.0, tk.END)

def toggle_theme():
    global dark_mode
    dark_mode = not dark_mode
    color_bg = "#1e1e1e" if dark_mode else "white"
    color_fg = "white" if dark_mode else "black"
    gui_output.configure(bg=color_bg, fg=color_fg)

# GUI Setup
root = tk.Tk()
root.title("PySniff - Enhanced GUI Packet Sniffer")
root.geometry("900x600")

# Interface dropdown
interface_var = tk.StringVar()
ttk.Label(root, text="Select Interface:").pack(pady=5)

# ✅ Correct way to get full interface info
interfaces = get_windows_if_list()
friendly_names = []

for iface in interfaces:
    name = f"{iface['name']} - {iface['description']}"
    guid = iface['guid']
    npf_device = f"\\Device\\NPF_{{{guid}}}"
    interface_map[name] = npf_device
    friendly_names.append(name)

interface_dropdown = ttk.Combobox(root, textvariable=interface_var, values=friendly_names, width=60)
interface_dropdown.pack()

# Filters
filter_frame = tk.Frame(root)
filter_frame.pack(pady=5)

ip_filter_var = tk.StringVar()
proto_filter_var = tk.StringVar(value="All")

ttk.Label(filter_frame, text="IP Filter:").grid(row=0, column=0, padx=5)
ttk.Entry(filter_frame, textvariable=ip_filter_var, width=20).grid(row=0, column=1, padx=5)

ttk.Label(filter_frame, text="Protocol Filter:").grid(row=0, column=2, padx=5)
ttk.Combobox(filter_frame, textvariable=proto_filter_var, values=["All", "TCP", "UDP", "ICMP"], width=10).grid(row=0, column=3, padx=5)

# Buttons
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

ttk.Button(button_frame, text="Start Sniffing", command=start_sniffing).grid(row=0, column=0, padx=8)
ttk.Button(button_frame, text="Stop", command=stop_sniff).grid(row=0, column=1, padx=8)
ttk.Button(button_frame, text="Export to TXT", command=export_to_txt).grid(row=0, column=2, padx=8)
ttk.Button(button_frame, text="Export to PCAP", command=export_to_pcap).grid(row=0, column=3, padx=8)
ttk.Button(button_frame, text="Clear Output", command=clear_output).grid(row=0, column=4, padx=8)
ttk.Button(button_frame, text="Dark Mode", command=toggle_theme).grid(row=0, column=5, padx=8)

# Packet display
gui_output = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=("Courier", 10), height=25)
gui_output.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

root.mainloop()
