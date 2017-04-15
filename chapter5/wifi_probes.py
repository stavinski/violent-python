#!/usr/bin/env python

from scapy.all import *

probes = []

def pkt_mon(pkt):
    if pkt.haslayer(Dot11ProbeReq):
        netName = pkt.getlayer(Dot11ProbeReq).info
        
        if netName not in probes:
            probes.append(netName)
            print "[+] new probe: %s" % netName

def main():
    print "[*] monitoring on iface wlan0mon"
    sniff(prn=pkt_mon, iface="wlan0mon")

if __name__ == "__main__":
    main()
