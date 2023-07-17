#!/usr/bin/python
import sys
import os
import subprocess
import signal
import time

# example command for ipmitool ----
#ipmitool  -H 172.30.0.54 -UADMIN -PADMIN i2c bus=1 chan=0 0xb8 <read_size> <write_d0> ; note adt7462 only one byte a time.

ipmi = "ipmitool -H "
login = " -UADMIN -PADMIN "
i2caddr = " 0xb8 "
sleep = "usleep 200000"
bufsize = 16
fantach = [0x98, 0x9a, 0x9c, 0x9e, 0xa2, 0xa4]
linespace = "-------------------------------------"


def run_cmd(cmd_str):
	#print cmd_str
	out, err = subprocess.Popen(cmd_str, stdout=subprocess.PIPE, shell=True).communicate()
	if len(out) < 2:
		print "I2C No return data, Stop....., check ip address, or bus number..."
		exit()
	return out

def getadt7462byte(ip, bus, offset):
	cmd = ipmi + ip + login + ' i2c bus=' + bus + ' ' + i2caddr + ' 1 ' + offset
	val = run_cmd(cmd)
	#print val
	return val.split('\n', 1)[0]

def getadt7462PID(ip, bus):
	pid = getadt7462byte(ip, bus, hex(0x3d) ) # read device id=0x62, and company ID =0x41
	vid = getadt7462byte(ip, bus, hex(0x3e) )# read device id=0x62, and company ID =0x41
	#print "pid, vid", pid, vid
	if ( int(pid, 16) == 0x62 and int(vid, 16) == 0x41 ):
		print linespace 
		print "Found ADT7462 PID=" + pid + " VID=" + vid  # there are string, so + together
		return 0
	else:
		print "CANNOT Find ADT7462"
		return 1

def changeFanMode(ip, bus, mode):
	cmd = ipmi + ip + login + ' i2c bus=' + bus + ' 0x20 ' + ' 1 ' + ' 0xcc ' 
	val =run_cmd(cmd)
	#print "Current Fan Mode = ", val,  "0=Man, 1=FC_PWM_HWM(default), 2=Auto, 3=MB PWM"
	cmd = ipmi + ip + login + ' i2c bus=' + bus + ' 0x20 ' + ' 0 ' + ' 0xcd ' + hex(mode)
	run_cmd(cmd)
	cmd = ipmi + ip + login + ' i2c bus=' + bus + ' 0x20 ' + ' 0 ' + ' 0xce ' + hex(0xa5)
	run_cmd(cmd)
	cmd = ipmi + ip + login + ' i2c bus=' + bus + ' 0x20 ' + ' 0 ' + ' 0xce ' + hex(0x5a)
	print "Change Fan Mode =", mode,  ".  Note: 0=Man, 1=FC_PWM_HWM(default), 2=Auto, 3=MB PWM"
	run_cmd(cmd)

def getadt7462speed(ip, bus):
	i = 0
	for fan in fantach:
		tach_lo = getadt7462byte(ip, bus, hex(fan) )
		tach_hi = getadt7462byte(ip, bus, hex(fan+1))
		tach = 90000*60/((int(tach_hi, 16) * 256)+int(tach_lo, 16)) 
		i += 1
		print "fan tach", i, '=', tach

def setadt7462Pwm(ip, bus, pwm):
	'''for offset in range(0x21,0x25):
		cmd = ipmi + ip + login + ' i2c bus=' + bus + ' 0xb8 ' + ' 1 ' + ' ' + hex(offset) + ' ' + hex(0xf1) # 0x21 is manual speed  
		print cmd
		val =run_cmd(cmd)
	'''
	for offset in range(0xaa,0xae):
		cmd = ipmi + ip + login + ' i2c bus=' + bus + ' 0xb8 ' + ' 1 ' + ' ' + hex(offset) + ' ' + hex(pwm) 
		val =run_cmd(cmd)

def getadt7462temp(ip, bus):
	temp = getadt7462byte(ip, bus, hex(0x89) )
	print "local temp = ", int(temp, 16) - 0x40
	temp = getadt7462byte(ip, bus, hex(0x8b) )
	print "D1    temp = ", int(temp, 16) - 0x40
	temp = getadt7462byte(ip, bus, hex(0x8d) )
	print "D2    temp = ", int(temp, 16) - 0x40
	temp = getadt7462byte(ip, bus, hex(0x8f) )
	print "D3    temp = ", int(temp, 16) - 0x40

def getadt7462volt(ip, bus):
	V12 = getadt7462byte(ip, bus, hex(0xa9) )
	print "Voltage(12)= ", round((int(V12, 16)*16.0*1000/255/1000),2), "[V]"

def main():
	if len(sys.argv) < 4:
        	print
        	print 'fanpwm: Fan pwm set '
        	print 'ex: fanpwm <ip_addr> <bus_num> <0-100>'
        	print 'ex: fanpwm 172.30.0.54 1 100'
        	print 'bus_num: 1 -> 2U, 3 -> 1U'
        	print 'try again'
        	exit()
	else:
        	ip = sys.argv[1]
        	bus_num = sys.argv[2]
		pwm = int(sys.argv[3])

	if ( getadt7462PID(ip, bus_num) == 0 ):	 # continue show data
		print linespace 
		changeFanMode(ip, bus_num, 0)
		speed = pwm*255/100 
		print linespace
		print "speed=", pwm,"%", "(", speed, ")"
		setadt7462Pwm(ip, bus_num, speed)
		time.sleep(3)
		getadt7462speed(ip, bus_num)

		print linespace
		raw_input( "press any key to continue")
		changeFanMode(ip, bus_num, 1)

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
