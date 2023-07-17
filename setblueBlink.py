#!/usr/bin/python
import sys
import os
import subprocess
import signal

# example command for ipmitool ----
#ipmitool  -H 172.30.0.54 -UADMIN -PADMIN i2c bus=1 chan=0 0xa4 <read_size> <write_d0> ;
#  Power Back Plane chip address is 0x5c

ipmi = "ipmitool -H "
login = " -UADMIN -PADMIN "
i2caddr = " 0x5c "
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
	#print cmd
	val = run_cmd(cmd)
	#print val
	return val.split('\n', 1)[0]

def setPowerBlue(ip, bus, addr, rate):
	Bin = setipmibyte(ip, bus, addr, hex(0x72), rate ) 
	
def main():
	if len(sys.argv) < 3:
        	print
        	print 'ex: setbluehi.py <ip_addr> <bus_num> <blinkRate>'
        	print 'ex: setbluehi.py 172.30.0.54 1 15'
		print 'rate is from 0-16, 0:off, 16:on'
        	print 'try again'
        	exit()
	else:
        	ip = sys.argv[1]
        	bus_num = sys.argv[2]
		#print len(sys.argv)
		if len(sys.argv) > 3:
			rate = sys.argv[3]
		else:
			rate = '0x0f'  

	print 'This is NOT NOT NOT JP4 Blue LED control from Riser.'
	print 'It is a power backplane Blue LED control, set to blinking mode'
	setPowerBlue(ip, bus_num, i2caddr, rate) 
	print 'set blink rate to', rate

if __name__ == '__main__':
    main()
