#########################################################
# Version 1
# Date: April 3, 2021
#
# This is the final version and should work
#
##########################################################
'''
This program will search for new workshop run every Friday.
The program will text to email when new workshop posted

SMS Message will send from Twilio account
User's email: amasterebay@gmail.com
pwd: Mydaughterjenna1!
'''

import time
import urllib.request as urllib2
#from twilio.rest import Client
#import html2text
#from bs4 import BeautifulSoup as Soup
import re
import subprocess
import time
import urllib.request as urllib2
#from twilio.rest import Client
from selenium import webdriver   
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, NoSuchWindowException, StaleElementReferenceException


#WS_details = "Homeowner101IndoorWorkshopC65"
#WS_details = "Homeowner101OutdoorWorkshopC48"
#WS_details = "Homeowner101SystemsWorkshopC60"


WS_details = "DIYHowtoStainaPatioandDeckC3"

WS_Base_Link = "https://events-na11.adobeconnect.com/content/connect/c1/2566155714/en/events/event/shared/2633997430/event_registration.html?sco-id="
'''
account_sid = "AC7c655561c461858c6785c936c34cf13a"
auth_token = "acd821fa6be6864b0e2216a6e1849270"
client = Client(account_sid, auth_token)
sleeptime = 120
myLoop = 0
'''
Match = 0
'''
page = urllib2.urlopen("https://events-na11.adobeconnect.com/content/connect/c1/2566155714/en/events/catalog.html?folder-id=2612902143&from-origin=thehomedepothomeowner101.adobeconnect.com")
content = page.read().decode('utf-8')Admin123!
print(content)

'''
#Search for new workshop"
while Match == 0 : # Run forever
    page = urllib2.urlopen("https://events-na11.adobeconnect.com/content/connect/c1/2566155714/en/events/catalog.html?folder-id=2612902143&from-origin=thehomedepothomeowner101.adobeconnect.com")
    content = page.read().decode('utf-8')
    time.sleep(30)  #time interval to search. Normally in 60 sec
    if WS_details in content:
        f = open("WS_log.txt", "w")
        f.write(content)
        f.close()

        with open("WS_log.txt") as file_iterator:
            for line in file_iterator:
                if WS_details in line:
                    if "sco-id" in line:
                        line_1 = line.split("sco-id=")[1]
                        SCO_ID= line_1.split('"')[0]
                        WS_Final_Link = WS_Base_Link + SCO_ID
                        print(SCO_ID)
                        print(WS_Final_Link)

        Match = 1
    print("Running")
    
'''
message = client.messages.create(
    to="+14086776803", 
    from_="+12059007160",
    body="New Workshop Found!")


'''
with open('emailDB.txt') as fp:
        for line in fp:
                Email = line.split("\t")[0]
                FirstN = line.split("\t")[3]
                LastN = line.split("\t")[4]
                Password = line.split("\t")[2]
                '''
                options = webdriver.ChromeOptions()
                options.add_argument('--proxy-server=%s' % "admin:admin123:185.242.111.51:12323")
                driver = webdriver.Chrome(options=options)
                '''
                driver = webdriver.Chrome()
                driver.set_window_size(1400,1000)
                #driver.get("https://events-na11.adobeconnect.com/content/connect/c1/2566155714/en/events/event/shared/2633997430/event_registration.html?sco-id=3094804680")
                driver.get(WS_Final_Link)
                while True:
                    try:
                        browser.find_element_by_id("login")
                    except:
                        break
                time.sleep(3)   # Time wait to enter the data
                registerEmail = driver.find_element_by_xpath("//*[@id='login']").send_keys(Email)
                time.sleep(1)
                registerEmail = driver.find_element_by_xpath("//*[@id='first-name']").send_keys(FirstN)
                time.sleep(1)
                registerEmail = driver.find_element_by_xpath("//*[@id='last-name']").send_keys(LastN)
                time.sleep(1)
                registerEmail = driver.find_element_by_xpath("//*[@id='password']").send_keys(Password)
                registerEmail = driver.find_element_by_xpath("//*[@id='password']").send_keys(Keys.TAB, Keys.TAB, Password, Keys.ENTER)
                time.sleep(100)
                driver.close()

fp.close()


