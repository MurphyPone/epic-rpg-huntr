from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from datetime import timedelta, date, datetime
import requests
import cv2

import math
import time
import json
import sys
import os
import random 

from conf import *


# ace = False

# Remove old files if present
def find_bj_score(driver):
    bjName = driver.find_elements_by_xpath("//img[@class='emoji']")
    lastNameNum = len(bjName) - 1
    lastName = bjName[lastNameNum]
    bjGame = lastName.find_element_by_xpath("./..")
    print(bjGame.text)
    bjStrBig = bjGame.text
    bjIn = int(bjStrBig.find("Total"))
    bjIn2 = int(bjIn+ 11)
    bjStr = bjStrBig[bjIn : bjIn2]
    # print(type(bjIn))
    # print(type (bjIn2))
    # print(bjStr)
    returnA = [int(i) for i in bjStr.split() if i.isdigit()] 
    # print("The numbers list is : " + str(returnA))
    returnI = returnA[0]
    # aceI = int(bjStrBig.find("~-~"))
    # aceI2 = aceI + 5
    # aceStr = bjStrBig[aceI: aceI2]
    # aceB = aceStr.find("A")
    # if aceB == -1:
    #     ace = True
    # else :
    #     ace =False
    return returnI

def find_bj_dealer_score(driver):
    bjName = driver.find_elements_by_xpath("//img[@class='emoji']")
    lastNameNum = len(bjName) - 1
    lastName = bjName[lastNameNum]
    bjGame = lastName.find_element_by_xpath("./..")
    print(bjGame.text)
    bjStrBig = bjGame.text
    bjIn = int(bjStrBig.rfind("Total"))
    bjIn2 = int(bjIn+ 11)
    bjStr = bjStrBig[bjIn : bjIn2]
    # print(type(bjIn))
    # print(type (bjIn2))
    # print(bjStr)
    returnA = [int(i) for i in bjStr.split() if i.isdigit()] 
    # print("The numbers list is : " + str(returnA))
    returnI = returnA[0]
    return returnI


# Used to delete old Firefox windows if they exist TODO determine if this is still even needed
def find_coin(driver, textBox):
        textBox.send_keys('RPG p')
        textBox.send_keys(Keys.RETURN)
        time.sleep(2)
        coinImgs = driver.find_elements_by_xpath("//img[@aria-label=':coin:']")
        last = len(coinImgs) - 1
        coinImg = coinImgs[last]
        coinAmnt = coinImg.find_element_by_xpath("./..")
     # print(coinAmnt)
        print(coinAmnt.text)
        coinTextBig = coinAmnt.text
        coinTextBig = coinTextBig.replace(",", "")
        res = [int(i) for i in coinTextBig.split() if i.isdigit()] 
    # print("The numbers list is : " + str(res))
        coinNumR = res[0]
        return coinNumR
def find_bet(coin) :
    prc = str(random.randint(3, (6) ))
    percS =  '0.0' + str(prc)
    perc = float(percS)
    sendR = str(int(coin * perc))
    return sendR
def login(driver):
    # Navigate to and login
    driver.get(URL)

    driver.find_element_by_name('email').send_keys(USER)
    driver.find_element_by_name('password').send_keys(PASS)
    # print(userIn)
    driver.find_element_by_xpath("//button[@type='submit']").click()
    # form = driver.find_element_by_xpath("//form")
    time.sleep(10)
    # form2 = form.find_element_by_xpath(".//*")
    # form2.click()
    # form2.send_keys("cock")
    textBox = driver.find_element_by_xpath("//div[@aria-label='Message #general']")
    
    # textBox.send_keys('RPG p')
    # textBox.send_keys(Keys.RETURN)
    # time.sleep(2)
    # coinImgs = driver.find_elements_by_xpath("//img[@aria-label=':coin:']")
    # last = len(coinImgs) - 1
    # coinImg = coinImgs[last]
    # coinAmnt = coinImg.find_element_by_xpath("./..")
    # # print(coinAmnt)
    # print(coinAmnt.text)
    # coinTextBig = coinAmnt.text
    # coinTextBig = coinTextBig.replace(",", "")
    # res = [int(i) for i in coinTextBig.split() if i.isdigit()] 
    # # print("The numbers list is : " + str(res))
    # coinNum = res[0]
    # print(coinNum)
    ender = True
    hit = 'hit'
    stay = 'stay'
    counterHunt = 0
    counterHeal = 0
    counterPickup = 0
    counterCF = 0
    while ender:
        counterHunt = counterHunt +1
        counterPickup = counterPickup +1
        counterCF = counterCF +1 
           
        time.sleep(2)
    #     textBox.send_keys('RPG p')
    #     textBox.send_keys(Keys.RETURN)
    #     time.sleep(2)
    #     coinImgs = driver.find_elements_by_xpath("//img[@aria-label=':coin:']")
    #     last = len(coinImgs) - 1
    #     coinImg = coinImgs[last]
    #     coinAmnt = coinImg.find_element_by_xpath("./..")
    #  # print(coinAmnt)
    #     print(coinAmnt.text)
    #     coinTextBig = coinAmnt.text
    #     coinTextBig = coinTextBig.replace(",", "")
    #     res = [int(i) for i in coinTextBig.split() if i.isdigit()] 
    # # print("The numbers list is : " + str(res))
    #     coinNum = res[0]
        coinNum = find_coin(driver, textBox)
        print(coinNum)
        if counterHunt >= 13 :
            counterHeal = counterHeal + 1
            if counterHeal == 2:
                textBox.send_keys('rpg buy life potion')
                textBox.send_keys(Keys.RETURN)
                time.sleep(1)
                textBox.send_keys('rpg heal')
                textBox.send_keys(Keys.RETURN)
                time.sleep(1)
                counterHeal = 0
            textBox.send_keys('rpg hunt')
            textBox.send_keys(Keys.RETURN) 
            time.sleep(1)
            counterHunt = 0
        if counterPickup >= 66 :
            textBox.send_keys('rpg chop')
            textBox.send_keys(Keys.RETURN)  
            counterPickup = 0
            time.sleep(1)  
            # coinH = int(coinNum / 2)
            # textBox.send_keys('rpg give @Alex Winstanley' + str(coinH))
            # textBox.send_keys(Keys.RETURN)                     

        if coinNum < 200 :
            textBox.send_keys('need coin bb @Alex Winstanley')
            textBox.send_keys(Keys.RETURN)
            return 
        bj = True
        # prc = str(random.randint(2, (8) ))
        # percS =  '0.0' + str(prc)
        # perc = float(percS)
        # send = str(int(coinNum * perc))
        sendCF = find_bet(coinNum)
        if counterCF >=5 :
            textBox.send_keys('RPG cf h ' + sendCF)
            textBox.send_keys(Keys.RETURN)
            time.sleep(1) 
            counterCF =0 
        sendD = find_bet(coinNum)
        textBox.send_keys('RPG dice ' + sendD)
        textBox.send_keys(Keys.RETURN)
        time.sleep(1) 
        sendC = find_bet(coinNum)
        textBox.send_keys('RPG cups ' + sendC)
        textBox.send_keys(Keys.RETURN)
        time.sleep(1) 
        cup = random.randint(1 , 3)
        textBox.send_keys(str(cup))
        textBox.send_keys(Keys.RETURN)
        time.sleep(1)         
        sendBJ = find_bet(coinNum)       
        textBox.send_keys('rpg bj '+ sendBJ)
        textBox.send_keys(Keys.RETURN)
        time.sleep(1)
        bjName = driver.find_elements_by_xpath("//img[@class='emoji']")
        lastNameNum = len(bjName) - 1
        lastName = bjName[lastNameNum]
        bjGame = lastName.find_element_by_xpath("./..")
        print(bjGame.text)
        bjStrBig = bjGame.text
        aceI = int(bjStrBig.find("~-~"))
        aceI2 = aceI + 5
        aceStr = bjStrBig[aceI: aceI2]
        aceB = aceStr.find("A")
        if aceB == -1:
            ace = True
        else :
            ace =False
        while bj :
            # textBox.send_keys('rpg bj 1')
            # textBox.send_keys(Keys.RETURN)
            time.sleep(1)
            score = find_bj_score(driver)
            print(score)
            dScore = find_bj_dealer_score(driver)
            print(dScore)
            if ace:
                if score == 21 and counterCF > 1:
                    textBox.send_keys(stay)
                    textBox.send_keys(Keys.RETURN)
                    time.sleep(1)
                    textBox.send_keys('RPG cf h ' + sendCF)
                    textBox.send_keys(Keys.RETURN)
                    time.sleep(1) 
                    bj = False 
                    ace = False
                elif score >= 19:
                    textBox.send_keys(stay)
                    textBox.send_keys(Keys.RETURN)
                    time.sleep(1)
                    bj = False  
                    ace = False
                elif score >= 18 and dScore >= 9:
                    textBox.send_keys(hit)
                    textBox.send_keys(Keys.RETURN)
                    time.sleep(1)
                    ace = False                                    
                elif score >= 18 : 
                    textBox.send_keys(stay)
                    textBox.send_keys(Keys.RETURN)
                    time.sleep(1)
                    bj = False  
                    ace = False
                else :
                    textBox.send_keys(hit)
                    textBox.send_keys(Keys.RETURN)
                    time.sleep(1)
                    ace = False                
            else :
                if score == 21 and counterCF > 1:
                    textBox.send_keys(stay)
                    textBox.send_keys(Keys.RETURN)
                    time.sleep(1)
                    textBox.send_keys('RPG cf h ' + sendCF)
                    textBox.send_keys(Keys.RETURN)
                    time.sleep(1) 
                    bj = False 
                elif score >= 17:
                    textBox.send_keys(stay)
                    textBox.send_keys(Keys.RETURN)
                    time.sleep(1)
                    bj = False                 
                elif 13 <= score <= 16 and dScore <= 6:
                    textBox.send_keys(stay)
                    textBox.send_keys(Keys.RETURN)
                    time.sleep(1)
                    bj = False 
                elif 13 <= score <= 16 and dScore > 6:
                    textBox.send_keys(hit)
                    textBox.send_keys(Keys.RETURN)
                    time.sleep(1)
                elif score == 12 and 4 >= dScore >= 6:
                    textBox.send_keys(stay)
                    textBox.send_keys(Keys.RETURN)
                    time.sleep(1)
                    bj = False 
                elif score == 12 and (4 > dScore or dScore > 6):  
                    textBox.send_keys(hit)
                    textBox.send_keys(Keys.RETURN)
                    time.sleep(1)
                elif score == 11:
                    textBox.send_keys(hit)
                    textBox.send_keys(Keys.RETURN)
                    time.sleep(1)
                else :
                    textBox.send_keys(hit)
                    textBox.send_keys(Keys.RETURN)
                    time.sleep(1)  
        coinNum2 = find_coin(driver, textBox)
        percent = coinNum * 0.10
            
        if (coinNum2 - percent) > coinNum:

            depo = int(coinNum2 * 0.02)
            depoStr= "rpg give @Alex Winstanley " + str(depo)
            textBox.send_keys(depoStr)
            textBox.send_keys(Keys.RETURN)
            time.sleep(1)              


            
    





    # driver.find_element(By.typeinput, "user_email1").click()
    # driver.find_element(By.ID, "user_email1").send_keys(USER)
    # driver.find_element(By.CSS_SELECTOR, "html").click()
    # driver.find_element(By.ID, "user_password").click()
    #driver.find_element(By.ID, "user_password").send_keys(PASS)
    # driver.find_element(By.ID, "user_password").submit()
    # driver.execute_script("window.scrollTo(0,0)")

d = build_driver()
login(d)

# def login():
#     # Navigate to and login
#     driver.get(URL)
#     driver.find_element(By.ID, "user_email1").click()
#     driver.find_element(By.ID, "user_email1").send_keys(USERNAME)
#     driver.find_element(By.CSS_SELECTOR, "html").click()
#     driver.find_element(By.ID, "user_password").click()
#     driver.find_element(By.ID, "user_password").send_keys(PASSWORD)
#     driver.find_element(By.ID, "user_password").submit()
#     driver.execute_script("window.scrollTo(0,0)")

#     # Nav to dashboard
#     time.sleep(10)
#     driver.find_element(By.ID, "dashboard-button").click()
#     time.sleep(10)
# URL = 'https://discordapp.com/login'
# page = requests.get(URL)

# # print (page.status_code)
# # print (page.headers)

# src = page.content
# soup = BeautifulSoup(src, 'html.parser')
# print(soup)
# cockinput = soup.find_all('input')
# print(cockinput)
