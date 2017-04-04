#!/usr/bin/env python

# MAC 2017-04-04 15:23:36

import sys
from zipfile import ZipFile

def main(zip_file, pwd_file):
    with ZipFile(zip_file) as zip, open(pwd_file, "r") as pwds:
        for line in pwds:
            pwd = line.strip("\n")
            try:
                zip.extractall(pwd=pwd)
                print "-" * 60
                print "[*] cracked password => [%s]" % pwd
                print "-" * 60
                return
            except RuntimeError:
                pass
    
    print "[-] could not crack password :("
            

if __name__ == "__main__":
  
    if len(sys.argv) < 3:
        exit("[!] usage %s zip_file password_file" % sys.argv[0])
      
main(sys.argv[1], sys.argv[2])
