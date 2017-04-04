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

def get_password(username):
  try:
    with open("/etc/shadow", "r") as shadow_file:
      lines = shadow_file.readlines()
      for line in lines:
        fields = line.strip("\n").split(":")
        if fields[0] == username:
          return fields[1]
      
      return None
  except IOError as e:
    exit("[!] error opening /etc/shadow file [%s], do you have permission to read this file?" % e.strerror)  

def crack_password(password_file, algo, salt, password):
  with open(password_file, "r") as password_file:
    for line in password_file:
      pwd = line.strip("\n")
      attempt = crypt.crypt(pwd, "$%s$%s" % (algo, salt)).split("$")[3]
  
      if password == attempt:
        print "*" * 60
        print "[*] cracked password => [%s]" % pwd
        print "*" * 60

def main(password_file, username):
  password = get_password(username)
  
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
    exit("[!] usage %s password_file username" % sys.argv[0])
  
  main(sys.argv[1], sys.argv[2])
