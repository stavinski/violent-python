#!/usr/bin/env python

import time
from bluetooth import *

# MAC 2017-04-16 13:35:58

found_devices = []

def find_devices():
    devices = discover_devices(lookup_names=True)
    for (addr, name) in devices:
        if addr not in found_devices:
            print "[*] found BT device: %s" % str(name)
            print "[+] MAC: %s" % str(addr)
            found_devices.append(addr)


def main():
    while True:
        find_devices()
        time.sleep(5)    

if __name__ == "__main__":
  main()
