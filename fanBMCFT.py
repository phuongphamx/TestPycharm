#!/usr/bin/python

import subprocess
import re
import os

def fancheckBMC(conn_number):
	f = "/home/admin/Desktop/TestReport/ReportTemp/%s.txt" %conn_number
	lines = subprocess.check_output(["ipmitool", "sdr", "type", "fan"]).decode("utf-8").splitlines()
	with open(f, "w") as out:
	    	for l in lines:
			print l
			out.write(l + "\n")
        		if re.search("(?=.*^(FAN3))(?!.*Source)(.+)",l):
            			l = l.replace (" ","")
	            		strBMC = l.split('|')[4]	
				fanBMCspeed = re.sub("\D","", strBMC)
				fanBMCspeed = int(fanBMCspeed)
			
				if (fanBMCspeed > 8600*1.25 or fanBMCspeed < 8600*0.75) :
                       			fanBMCstatus = "FAILED"
               			else:
					fanBMCstatus = "PASSED"
	out.close()
	return fanBMCstatus

