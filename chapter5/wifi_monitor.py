#!/usr/bin/env python

from scapy.all import *

def pkt_mon(pkt):
    if pkt.haslayer(Dot11Beacon):
        print "[+] detected 802.11 beacon frame"
    elif pkt.haslayer(Dot11ProbeReq):
        print "[+] detected 802.11 probe request"
    elif pkt.haslayer(TCP):
        print "[+] detected TCP packet"
    elif pkt.haslayer(DNS):
        print "[+] detected DNS packet"


def main():
    print "[*] monitoring on iface wlan0mon"
    sniff(prn=pkt_mon, iface="wlan0mon")

if __name__ == "__main__":
    main()
