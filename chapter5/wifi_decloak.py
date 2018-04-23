#!/usr/bin/env python

# decloak hidden ssids

import sys
import threading

from scapy.all import *

hidden = set()
unhidden = set()


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
    if pkt.haslayer(Dot11ProbeResp):
      addr2 = pkt[Dot11].addr2
      if addr2 in hidden and addr2 not in unhidden:
        name = pkt[Dot11ProbeResp].info
        print "[+] de-cloaked hidden ssid: %s -> %s" % (addr2, name)
        unhidden.append(addr2)

    if pkt.haslayer(Dot11Beacon):
      if pkt[Dot11Beacon].info == "":
        addr2 = pkt[Dot11].addr2
        if addr2 not in hidden:
          print "[-] detected hidden ssid: %s" % addr2
          hidden.append(addr2)


def main():
    if len(sys.argv) < 2:
      sys.exit("[!] usage: %s [iface]" % sys.argv[0])

    iface = sys.argv[1]

    print "[*] starting channel hopper"
    wt_channel_hopper = threading.Thread(target=channel_hopper, args=(iface,))
    wt_channel_hopper.daemon = True
    wt_channel_hopper.start()

    print "[*] monitoring on iface %s" % iface
    sniff(prn=pkt_mon, iface=iface, store=0)

if __name__ == "__main__":
    main()
