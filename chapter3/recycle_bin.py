import os
import _winreg

from argparse import ArgumentParser

def recycle_bin_dir():
	dirs = ["c:\\Recycler\\", "c:\\Recycled\\", "c:\\$Recycle.Bin\\"]
	for dir in dirs:
		if os.path.isdir(dir):
			return dir

	return None
	
def sid_to_username(sid):
	try:
		sid_key = "SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\ProfileList\\%s" % sid
		key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, sid_key, 0, _winreg.KEY_READ | _winreg.KEY_WOW64_64KEY)
		(value, type) = _winreg.QueryValueEx(key, "ProfileImagePath")
		return value.split("\\")[-1]
	except: # could not get username
		return sid
			
def main():
	parser = ArgumentParser("recycle bin util")

	parser.add_argument("-s", "--show", action="store_true", help="show entries for all users")
	parser.add_argument("-u", "--user", help="user to copy files for")
	parser.add_argument("-o", "--output", help="output dir for copied files (default c:\\temp)", default="c:\\temp\\")
	
	args = parser.parse_args()
	
	search_dir = recycle_bin_dir()
	print "[*] recycle bin: %s" % search_dir
	
	if args.show:
		for sid in os.listdir(search_dir):
			files = os.listdir(os.path.join(search_dir, sid))
			user = sid_to_username(sid)
			print "[*] files for user: %s" % user
			for file in files:
				print "\t[+] %s" % file
	
	if args.user is not None:
		for sid in os.listdir(search_dir):
			user = sid_to_username(sid)
			if args.user == user:
				print "[+] copying directory for user to %s" % args.output
				os.system("XCOPY %s %s /Y /E /C /I /F /H" % (os.path.join(search_dir, sid), args.output))
	
if __name__ == "__main__":
	main()