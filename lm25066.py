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
i2caddr = " 0xa4 "
i2caddr2 = " 0xa6 "
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

def getlm25066PID(ip, bus, addr):
	pid = getipmibyte(ip, bus, addr, hex(0x9a), hex(9) ) # MFR ID : 4c 4d 32 35 30 36 36 00, rev 41 41
	#print "pid=", pid
	mfgid = pid.split()
	if ( int(mfgid[1], 16) == 0x4c and int(mfgid[2],16) == 0x4d and int(mfgid[3],16) == 0x32 ):
		print linespace 
		print "Found LM25066 (" + addr +")" + pid 
		return 0
	else:
		print "CANNOT Find Device LM25066"
		return 1

def getlm25066Vin(ip, bus, addr):
	vin = getipmibyte(ip, bus, addr, hex(0x88), hex(2) )
	readv = vin.split()
	v0 = int(readv[0], 16)
	v1 = int(readv[1], 16)
	#print v0, v1
	volt = ( (v0+v1*256)*100.0 + 1800.0)/22070.0
	print "Read Vin  =", round(volt, 3), "V"

def getlm25066Vout(ip, bus, addr):
	vin = getipmibyte(ip, bus, addr, hex(0x8b), hex(2) )
	readv = vin.split()
	v0 = int(readv[0], 16)
	v1 = int(readv[1], 16)
	#print v0, v1
	volt = ( (v0+v1*256)*100.0 + 1800.0)/22070.0
	print "Read Vout =", round(volt, 3), "V"

def getlm25066AvgIin(ip, bus, addr):
	vin = getipmibyte(ip, bus, addr, hex(0xde), hex(2) )
	readv = vin.split()
	v0 = int(readv[0], 16)
	v1 = int(readv[1], 16)
	#print v0, v1
	volt = ( (v0+v1*256)*100.0 + 5200.0)/(13661.0*0.75)
	print "Read Iin  =", round(volt, 3), "A"

def main():
	if len(sys.argv) < 2:
        	print
        	print 'ex: lm25066 <ip_addr> <bus_num>'
        	print 'ex: lm25066 172.30.0.5 1'
        	print 'try again'
        	exit()
	else:
        	ip = sys.argv[1]
        	bus_num = sys.argv[2]

	if ( getlm25066PID(ip, bus_num, i2caddr) == 0 ):	 # continue show data
		print linespace 
		getlm25066Vin(ip, bus_num, i2caddr)
		print linespace 
		getlm25066Vout(ip, bus_num, i2caddr)
		print linespace 
		getlm25066AvgIin(ip, bus_num, i2caddr)

	if ( getlm25066PID(ip, bus_num, i2caddr2) == 0 ):	 # continue show data
		print linespace 
		getlm25066Vin(ip, bus_num, i2caddr2)
		print linespace 
		getlm25066Vout(ip, bus_num, i2caddr2)
		print linespace 
		getlm25066AvgIin(ip, bus_num, i2caddr2)

if __name__ == '__main__':
    main()
