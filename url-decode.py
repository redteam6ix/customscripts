#!/bin/python3

import sys
#import os

if (len(sys.argv) > 2):
	print("Usage: urlencode.py [<cmd>]")
	print("No arguments = interactive mode (\"exit\" to exit)")
	print("You may need to manually switch some special chars")
	sys.exit(0)

#### need to define letters, numbers, etc.

def decode(cmd):
	decoded=cmd
	decoded=decoded.replace("%25","%")
	decoded=decoded.replace("%20"," ")
	decoded=decoded.replace("%21","!")
	decoded=decoded.replace("%40","@")
	decoded=decoded.replace("%23","#")
	decoded=decoded.replace("%24","$")
	decoded=decoded.replace("%5E","^")
	decoded=decoded.replace("%26","&")
	decoded=decoded.replace("%2A","*")
	decoded=decoded.replace("%28","(")
	decoded=decoded.replace("%29",",)")
	decoded=decoded.replace("%2D","-")
	decoded=decoded.replace("%3D","=")
	decoded=decoded.replace("%2B","+")
	decoded=decoded.replace("%2C",",")
	decoded=decoded.replace("%2E",".")
	decoded=decoded.replace("%2F","/")
	decoded=decoded.replace("%5C","\\")
	decoded=decoded.replace("%7E","~")
	decoded=decoded.replace("%60","`")
	decoded=decoded.replace("%27","'")
	decoded=decoded.replace("%22","\"")
	decoded=decoded.replace("%3B",";")
	decoded=decoded.replace("%3A",":")
	decoded=decoded.replace("%7C","|")
	decoded=decoded.replace("%3C","<")
	decoded=decoded.replace("%3E",">")
	decoded=decoded.replace("%5B","[")
	decoded=decoded.replace("%5D","]")
	decoded=decoded.replace("%7B","{")
	decoded=decoded.replace("%7D","}")
	decoded=decoded.replace("%5F","_")
	decoded=decoded.replace("%3F","?")

	return decoded

#site=sys.argv[1]
if (len(sys.argv) > 1):
	print(decode(sys.argv[1]))
	sys.exit(0)

rawcmd=""
while (rawcmd != "exit"):
	if (rawcmd == "exit"):
		sys.exit(0)	
	rawcmd=input("url-decode> ")
	print(decode(rawcmd))

#print(encode(sys.argv[1]))
