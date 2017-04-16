#!/usr/bin/env python

import sys
from argparse import ArgumentParser
from bluetooth import *

# MAC 2017-04-16 13:59:39

def main(mac_file):
    with open(mac_file, "r") as macs:
        for mac in macs:
            test = str(mac).strip("\n")
            name = lookup_name(test)
            if name:
                print "[+] %s => %s" % (test, name)
            else:
                print "[-] %s" % test

if __name__ == "__main__":
    parser = ArgumentParser("BT prober")
    parser.add_argument("mac_file", help="file with BT MACS to probe for", type=str)

    args = parser.parse_args()
    main(args.mac_file)
