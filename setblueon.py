#!/usr/bin/python
import sys
import os
import subprocess
import signal

# example command for ipmitool ----
#ipmitool  -H 172.30.0.54 -UADMIN -PADMIN i2c bus=1 chan=0 0xa4 <read_size> <write_d0> ;
#  tmax chip address is 0x20

ipmi = "ipmitool -H "
login = " -UADMIN -PADMIN "
i2caddr = " 0x20 "
sleep = "usleep 200000"
bufsize = 16
linespace = "------------------------------------------"


def run_cmd(cmd_str):
	out, err = subprocess.Popen(cmd_str, stdout=subprocess.PIPE, shell=True).communicate()
	if len(out) < 2:
		print "I2C No return data, Stop....., check IP address, or BUS number..."
		exit()
	return out

def getipmibyte(ip, bus, addr, offset, length):
	cmd = ipmi + ip + login + ' i2c bus=' + bus + ' ' + addr + length +' '+ offset
	#print cmd
	val = run_cmd(cmd)
	#print val
	return val.split('\n', 1)[0]

def setipmibyte(ip, bus, addr, offset, byte0 ):
	cmd = ipmi + ip + login + ' i2c bus=' + bus + ' ' + addr + ' 0 '+ offset + ' ' + byte0
	print cmd
	val = run_cmd(cmd)
	print val
	return val.split('\n', 1)[0]

def setport1(ip, bus, addr):
	Bin = setipmibyte(ip, bus, addr, hex(0xc3), hex(0x08) )
	Bin = setipmibyte(ip, bus, addr, hex(0xc4), hex(0xa5) )
	Bin = setipmibyte(ip, bus, addr, hex(0xc4), hex(0x5a) )
	
	
def main():
	if len(sys.argv) < 2:
        	print
        	print 'ex: setbluehi.py <ip_addr> <bus_num>'
        	print 'ex: setbluehi.py 172.30.0.54 1'
        	print 'try again'
        	exit()
	else:
        	ip = sys.argv[1]
        	bus_num = sys.argv[2]

	print 'This is JP4 Blue LED control, Which may not connect to a LED'
	setport1(ip, bus_num, i2caddr) 

if __name__ == '__main__':
    main()
