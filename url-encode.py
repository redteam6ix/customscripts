#!/bin/python3

import sys
#import os

if (len(sys.argv) > 2):
	print("Usage: urlencode.py [<cmd>]")
	print("No arguments = interactive mode (\"exit\" to exit)")
	print("You may need to manually switch some special chars")
	sys.exit(0)


def encode(cmd):
	encoded=cmd
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

#site=sys.argv[1]
if (len(sys.argv) > 1):
	print(encode(sys.argv[1]))
	sys.exit(0)

rawcmd=""
while (rawcmd != "exit"):
	if (rawcmd == "exit"):
		sys.exit(0)	
	rawcmd=input("url-encode> ")
	print(encode(rawcmd))

#print(encode(sys.argv[1]))
