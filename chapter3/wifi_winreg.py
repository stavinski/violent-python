from _winreg import *

base_key = "SOFTWARE\Microsoft\Windows NT\CurrentVersion\NetworkList\Signatures\Unmanaged"

def bin2macaddr(val):
	hex = ["%02x" % ord(x) for x in val][:6] 
	return reduce((lambda x, y: x + ":" + y), hex)

def main():
	key = OpenKey(HKEY_LOCAL_MACHINE, base_key, 0, KEY_READ | KEY_WOW64_64KEY)
	print "[*] Networks joined:"
	
	for i in range(100):
		try:
			guid = EnumKey(key, i)
			netkey = OpenKey(key, str(guid))
			(n, addr, t) = EnumValue(netkey, 5)
			(n, name, t) = EnumValue(netkey, 4)
			
			if not addr is None:
				mac = bin2macaddr(addr)
				print "[%s] => %s" % (name, mac)

			CloseKey(netkey)
		except WindowsError as e:
			break
	
	
if __name__ == "__main__":
	main()