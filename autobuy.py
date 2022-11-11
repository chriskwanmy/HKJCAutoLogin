from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup
import re
import requests
import pandas as pd
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials

from urllib import request
import json
from datetime import date
from datetime import datetime
scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json",scope)
client = gspread.authorize(creds)

racingno=2

driver = webdriver.Firefox()
driver.get("https://bet.hkjc.com/racing/pages/odds_wpq.aspx?lang=ch&date=2020-06-14&venue=ST&raceno=2")
sheet2 = client.open("temp").get_worksheet(1)
# driver.find_element_by_xpath("""//*[@id="page-wrapper"]/div[2]/div/div/div[2]/div[2]/div/button""").click()
time.sleep(0.2)
driver.find_element_by_id("account").send_keys("username")
# driver.find_element_by_id("passwordInput1").send_keys("nigo1994512")
time.sleep(0.2)
driver.find_element_by_xpath("""//*[@id="passwordInput1"]""").click()
driver.find_element_by_id("password").send_keys("password")
driver.find_element_by_id("loginButton").click()
time.sleep(0.2)
question=driver.find_element_by_id("ekbaSeqQuestion").text
print("answering question")
driver.find_element_by_xpath("""//*[@id="ekbaDivInput"]""").click()
time.sleep(0.2)
driver.find_element_by_xpath("""//*[@id="ekbaDivInput"]""").click()
if question=="first security question":
    driver.find_element_by_id("ekbaDivInput").send_keys("first answer")
elif question=="second security question":
    driver.find_element_by_id("ekbaDivInput").send_keys("second answer")
else:
    driver.find_element_by_id("ekbaDivInput").send_keys("third answer")
driver.find_element_by_class_name("confirmButton").click()
print("Logged in")
time.sleep(1)
driver.find_element_by_id("disclaimerProceed").click()
contin=input("1 to conyinue")

result1= sheet2.acell('B15').value
# result1 = input("please input racenumber,first-second,.....x10")
print(result1)
# sheet2.update_acell('u46', 'Bingo!')
result = result1.split(",")
buyhorse = []

for data in result:
    if (len(data)<3):
        raceno=int(data)
        continue
    else:
        buyhorse.append(data)

print("Buyhorse ready. waiting for 5s")
time.sleep(1)


# driver.find_element_by_id("raceSel" + str(racingno)).click()
# ['1-2', '3-4', '5-6', '7-8', '9-10', '8-9', '7-5', '2-4', '5-9', '3-8']

for data in buyhorse:
    data1 = data.split("-")
    bought=False
    if (int(data1[0])<=7):
        while (bought==False):
            
            driver.find_element_by_xpath("""//*[@id="combOddsTableQIN"]/table/tbody/tr["""+str(int(data1[0])+1)+"""]/td["""+str(int(data1[1])+2)+"""]""").click()
            print("buy "+ str(data1[0]) + "-" + str(data1[1]))
            bought = True
    else:
        while (bought==False):
            driver.find_element_by_xpath("""//*[@id="combOddsTableQIN"]/table/tbody/tr["""+str(int(data1[1])-6)+"""]/td["""+str(int(data1[0])-6)+"""]""").click()
            print("buy "+ str(data1[0]) + "-" + str(data1[1]))
            bought = True
    #//*[@id="combOddsTableQIN"]/table/tbody/tr[3]/td[2]
driver.find_element_by_id("bsSendPreviewButton").click()


# //*[@id="combOddsTableQIN"]/table/tbody/tr[2]/td[12]/a
# [1,1-2,3-4,5-6,7-8,9-10,8-9,5-7,4-6,5-9,3-8]
