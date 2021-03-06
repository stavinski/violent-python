#!/usr/bin/env python

import sys
import threading

from scapy.all import *

probes = []

def channel_hopper(iface):
  channels = list(range(1, 14))

  while True:
    try:
      channel = random.choice(channels)
      os.system("iw dev %s set channel %d" % (iface, channel))
      time.sleep(1)
    except e:
      print "[!] error channel hopping: %s" % e



def pkt_mon(pkt):
    if pkt.haslayer(Dot11ProbeReq):
        netName = pkt.getlayer(Dot11ProbeReq).info

        if netName not in probes:
            probes.append(netName)
            print "[+] new probe: %s" % netName

def main():
    if len(sys.argv) < 2:
      sys.exit("[!] usage: %s [iface]" % sys.argv[0])

    iface = sys.argv[1]

    print "[*] starting channel hopper"
    wt_channel_hopper = threading.Thread(target=channel_hopper, args=(iface,))
    wt_channel_hopper.daemon = True
    wt_channel_hopper.start()

    print "[*] monitoring on iface %s" % iface
    sniff(prn=pkt_mon, iface=iface)

if __name__ == "__main__":
    main()
