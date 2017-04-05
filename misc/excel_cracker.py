#!/usr/bin/env python

import sys
import os
import win32com.client as win32
import pywintypes

# com error no for invalid password
PASSWORD_ERR_NO = -2147352567

def main(excel_file, pwd_file):
	
	if not os.path.exists(excel_file):
		print "[!] could not find excel file"
		exit(1)

	excel = win32.gencache.EnsureDispatch('Excel.Application')
	excel.Visible = False
	
	with open(pwd_file, "r") as pwds:
		for line in pwds:
			pwd = line.strip("\n")
			try:
				wb = excel.Workbooks.Open(excel_file, Password=pwd)
				print "-" * 60
				print "[*] password cracked => [%s]" % pwd
				print "-" * 60
				exit(0)
				
			except pywintypes.com_error as e:
				if e[0] == PASSWORD_ERR_NO:
					pass
				else:
					print "[!] error raised opening: %s" % str(e)
					exit(1)

	print "[-] could not crack password :("

if __name__ == "__main__":
	if len(sys.argv) < 3:
		print "[!] usage: %s excel_file password_file" % sys.argv[0]
		exit(0)

	main(sys.argv[1], sys.argv[2])
