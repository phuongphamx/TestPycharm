#########################################################
# Version 1
# Date: April 3, 2021
#
# This is the final version and should work
#
##########################################################

import re
import subprocess
import time
from datetime import datetime
import urllib.request as urllib2
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, NoSuchWindowException, StaleElementReferenceException
from pathlib import Path, PurePath

seller_Id = []
seller_link = []
seller_field = []
sales_number = []
i = 0

format_time = time.localtime()
format_time = time.strftime("%m%d%Y", format_time)
file_name = format_time + '_EtsyWatch'+'.txt'
file_name_path = Path('D:','/','Etsy',file_name)
file_list_path = Path('D:','/','Etsy','EtsyList.txt')

def write_RPT(file_name_path,seller_Id, seller_field, sales_number):
    index = 0
    file_rpt = open(file_name_path, 'w')
    file_rpt.write("{:30}{:40}{:20}\n".format("SellerID","SellerField",format_time))
    while index < len(seller_Id):
        file_rpt.write("{:30}{:40}{:20}\n".format(seller_Id[index], seller_field[index], sales_number[index]))
        index = index + 1
with open(file_list_path, "r") as f_read:
    for line in f_read:
            seller_Id.append(line.split("\t")[0])
            seller_field.append(line.split("\t")[1].strip("\n"))
f_read.close()


while i < len(seller_Id):
    fname = seller_Id[i]+'.txt'
    fname_path = Path('D:','/','Etsy',fname)
    page_str = 'https://www.etsy.com/shop/'+seller_Id[i]+'?ref=shop_sugg'
    page = urllib2.urlopen(page_str)
    content = page.read().decode('utf-8')

    with open(fname_path, "w", encoding="utf-8") as f:
        f.write(content)
        f.close()

    with open(fname_path, "r", encoding="utf-8") as file_iterator:
        for line in file_iterator:
            match_str_1 = '/shop/'+ seller_Id[i]+'/sold'
            match_str_2 = 'wt-text-caption wt-no-wrap'
            if (match_str_1 in line):
                line_1 = line.split(match_str_1)[1]
                line_1 = line_1.split(">")[1]
                sales_number.append(line_1.split(" ")[0].strip())
                break
            elif (match_str_2 in line):
                line_1 = line.split(">")[1]
                sales_number.append(line_1.split(" ")[0].strip())
                break
    i = i+1

write_RPT(file_name_path,seller_Id, seller_field, sales_number)