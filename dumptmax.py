#!/usr/bin/python
import sys
import os
import subprocess
import signal

# example command for ipmitool ----
#ipmitool  -H 172.30.0.54 -UADMIN -PADMIN i2c bus=1 chan=0 0xa4 <read_size> <write_d0> ;
# lm25066 address has been remapped to 0xa4, and 0xa6 by tmax chip 

ipmi = "ipmitool -H "
login = " -UADMIN -PADMIN "
# 0x20 is TMAX slave address.....
i2caddr = " 0x20 "
sleep = "usleep 500000"
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
	print val
	return val.split('\n', 1)[0]

def main():
	if len(sys.argv) < 2:
        	print
        	print 'ex: getport12 <ip_addr> <bus_num, [1|3]>'
        	print 'ex: getport12 172.30.0.54 1'
        	print 'try again'
        	exit()
	else:
        	ip = sys.argv[1]
        	bus_num = sys.argv[2]

	getipmibyte(ip, bus_num, i2caddr, " 0x00 ", " 0x40")
	sleep
	getipmibyte(ip, bus_num, i2caddr, " 0x40 ", " 0x40")
	sleep
	getipmibyte(ip, bus_num, i2caddr, " 0x80 ", " 0x40")
	sleep
	getipmibyte(ip, bus_num, i2caddr, " 0xc0 ", " 0x40")

if __name__ == '__main__':
    main()
