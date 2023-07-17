#!/usr/bin/python
import sys
import os
import subprocess
import signal
import time

# example command for ipmitool ----
#ipmitool  -H 172.30.0.54 -UADMIN -PADMIN i2c bus=1 chan=0 0xb8 <read_size> <write_d0> ; 
# note at24mac402 's MAC is mapped to 0xa2 

ipmi = "ipmitool -H "
login = " -UADMIN -PADMIN "
i2caddr = " 0xa2 "
sleep = "usleep 200000"
bufsize = 16
linespace = "------------------------------------------------"


def run_cmd(cmd_str):
	#print cmd_str
	out, err = subprocess.Popen(cmd_str, stdout=subprocess.PIPE, shell=True).communicate()
	if len(out) < 2:
		print "I2C No return data, Stop....., check ip address, or bus number..."
		exit()
	return out

def getipmibyte(ip, bus, offset, size):
	cmd = ipmi + ip + login + ' i2c bus=' + bus + ' ' + i2caddr + ' ' + hex(size) + ' ' + hex(offset)
	val = run_cmd(cmd)
	return val.split('\n', 1)[0]

def getat24msn(ip, bus):
	print "at24mac - Serial Number"
	print getipmibyte(ip, bus, 0x80, 0x10)
def getat24m48(ip, bus):
	print "at24mac - EUI-48"
	print getipmibyte(ip, bus, 0x9a, 0x06)
def getat24m64(ip, bus):
	print "at24mac - EUI-64"
	print getipmibyte(ip, bus, 0x98, 0x08)

def main():
	if len(sys.argv) < 3:
        	print
        	print 'at24m: Display serial EEP S/N, and UEI-48/64'
        	print 'ex: at24m <ip_addr> <bus_num>'
        	print 'ex: at24m 172.30.0.54 1'
        	print 'try again'
        	exit()
	else:
        	ip = sys.argv[1]
        	bus_num = sys.argv[2]

	print linespace 
	getat24msn(ip, bus_num)
	getat24m48(ip, bus_num)
	getat24m64(ip, bus_num)

def exit_gracefully(signum, frame):
	global original_sigint
	# restore the original signal handler as otherwise evil things will happen
	# in raw_input when CTRL+C is pressed, and our signal handler is not re-entrant
	signal.signal(signal.SIGINT, original_sigint)
	print("OK, quitting")
	# close anything else here too
	sys.exit(1)

if __name__ == '__main__':
	global original_sigint
	original_sigint = signal.getsignal(signal.SIGINT)
	signal.signal(signal.SIGINT, exit_gracefully)	
	main()
