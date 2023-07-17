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

def getport1(ip, bus, addr):
	Bin = getipmibyte(ip, bus, addr, hex(0xc5), hex(1) )
	print "port 1, in  =", Bin
	BinVal = int(Bin,16)
	if ( BinVal & 0x01 ):
		print "P1.0, TP12            : Hi"
	else:
		print "P1.0, TP12            : Lo"
	if ( BinVal & 0x08 ):
		print "P1.3, FRU_WPROT       : Hi"
	else:
		print "P1.3, FRU_WPROT       : Lo"
	if ( BinVal & 0x10 ):
		print "P1.4, MB_FC_L         : Hi"
	else:
		print "P1.4, MB_FC_L         : Lo"
	if ( BinVal & 0x20 ):
		print "P1.5, BLUE_LED_CTRL_L : Hi"
	else:
		print "P1.5, BLUE_LED_CTRL_L : Lo"
	if ( BinVal & 0x40 ):
		print "P1.6, HB              : Off"
	else:
		print "P1.6, HB              : On"	
	if ( BinVal & 0x80 ):
		print "P1.7, SEL_BLUE-PWRLED : Hi"
	else:
		print "P1.7, SEL_BLUE-PWRLED : Lo"
	
def getport2(ip, bus, addr):
	Bin = getipmibyte(ip, bus, addr, hex(0xc6), hex(1) )
	print "port 2, in  =", Bin
	BinVal = int(Bin,16)
	if ( BinVal & 0x10 ):
		print "P2.4, PS_PWRGOOD_N    : Hi"
	else:
		print "P2.4, PS_PWRGOOD_N    : Lo"
	if ( BinVal & 0x20 ):
		print "P2.5, ADT7462_ALERT_L : Hi"
	else:
		print "P2.5, ADT7462_ALERT_L : Lo"
	if ( BinVal & 0x40 ):
		print "P2.6, UID_LED_STATUS  : Hi"
	else:
		print "P2.6, UID_LED_STATUS  : Lo"
	if ( BinVal & 0x80 ):
		print "P2.7, TP11            : Hi"
	else:
		print "P2.7, TP11            : Lo"
def main():
	if len(sys.argv) < 2:
        	print
        	print 'ex: getport12.py <ip_addr> <bus_num>'
        	print 'ex: getport12.py 172.30.0.54 1'
        	print 'try again'
        	exit()
	else:
        	ip = sys.argv[1]
        	bus_num = sys.argv[2]

	getport1(ip, bus_num, i2caddr) 
	getport2(ip, bus_num, i2caddr) 

if __name__ == '__main__':
    main()
