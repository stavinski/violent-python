#!/usr/bin/env python

# MAC 2017-04-04 08:31:51

import sys
import crypt

algos = { 
  "1": "MD5",
  "2a": "Blowfish",
  "2y": "Blowfish 8 bit chars",
  "5": "sha256",
  "6": "sha512"
}

def get_password(shadow_file, username):
  try:
    with open(shadow_file, "r") as shadow_file:
      lines = shadow_file.readlines()
      for line in lines:
        fields = line.strip("\n").split(":")
        if fields[0] == username:
          return fields[1]
      
      return None
  except IOError as e:
    exit("[!] error opening: '%s' - [%s], do you have permission to read this file?" % (shadow_file, e.strerror))  

def crack_password(password_file, algo, salt, password):
  with open(password_file, "r") as password_file:
    for line in password_file:
      pwd = line.strip("\n")
      attempt = crypt.crypt(pwd, "$%s$%s" % (algo, salt)).split("$")[3]
  
      if password == attempt:
        print "*" * 60
        print "[*] cracked password => [%s]" % pwd
        print "*" * 60
        return
    
    print "[-] could not crack password :("

def main(password_file, username, shadow_file="/etc/shadow"):
  password = get_password(shadow_file, username)
  
  if password is None:
    print "[!] could not find [%s]" % username
    exit(0)
  
  if password == "*":
    print "[!] username does not have password to crack"
    exit(0)
  
  if password == "!":
    print "[!] password retrieved could not be cracked"
    exit(0)
  
  _, algo, salt, password = password.split("$")
  
  
  print "[+] algo: %s" % algos[algo]
  print "[+] salt: %s" % salt
  print "[+] password: %s" % password
  
  crack_password(password_file, algo, salt, password)
  
if __name__ == "__main__":
  if len(sys.argv) < 3:
    exit("[!] usage %s password_file username [shadow_file]" % sys.argv[0])
  
  if len(sys.argv) == 4:
    main(sys.argv[1], sys.argv[2], sys.argv[3])
  else:
    main(sys.argv[1], sys.argv[2])
  