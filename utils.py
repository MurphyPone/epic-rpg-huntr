from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from datetime import timedelta, date, datetime

import shutil
import requests

import cv2 
import pytesseract
import time
import re

from conf import *


# Configure web driver
def build_driver():
    cap = DesiredCapabilities().FIREFOX
    if OS == "OSX": 
        executable_path = "./drivers/geckodriver"
    elif OS == "Windows":
        executable_path = "./drivers/geckodriver.exe" 
    return webdriver.Firefox(capabilities=cap, executable_path=executable_path)

# Login to personal discord server
def login(driver):
    driver.get(URL)     
    driver.find_element_by_name('email').send_keys(USER)
    driver.find_element_by_name('password').send_keys(PASS)
    driver.find_element_by_xpath("//button[@type='submit']").click()
    time.sleep(10)

# sends a message
def send_message(driver, msg):
    mesg_element = driver.find_element_by_xpath(f"//div[@aria-label='Message {CHANNEL_NAME}']")
    mesg_element.send_keys(msg)
    mesg_element.send_keys(Keys.RETURN)
    print(f"Sent message: '{msg}'")
    time.sleep(2)
    detect_captcha(driver)
    return 

# heals the player
def heal(driver):
    send_message(driver, "rpg heal")

# ensures the player is at max health, then hunts
def hunt(driver):
    stats = get_stats(driver)
    if get_hp_as_pct(stats) < 0.8:
        buy_life_potion(driver)
        heal(driver)

    send_message(driver, "rpg hunt")

# Safely does an adventure
def adventure(driver):
    buy_life_potion(driver)
    heal(driver)
    send_message(driver, "rpg adventure")

# Gathers in the first area
def gather_1(driver, count, focus="even"):
    if focus == "even":
        print(f"COUNT: {count}")
        if(count % 2 == 0):
            send_message(driver, "rpg chop")
        else: 
            send_message(driver, "rpg fish")

    if focus == "wood":
        send_message(driver, "rpg chop")
    if focus == "fish":
        send_message(driver, "rpg fish")
    
    count = count + 1

# Gathers in the third area
def gather_3(driver, count, focus="even"):
    if focus == "even":
        print(f"COUNT: {count}")
        if(count % 3 == 0):
            send_message(driver, "rpg axe")
        elif(count % 3 == 1): 
            send_message(driver, "rpg net")
        elif(count % 3 == 2): 
            send_message(driver, "rpg pickup")

    if focus == "wood":
        send_message(driver, "rpg axe")
    if focus == "fish":
        send_message(driver, "rpg net")
    if focus == "apple":
        send_message(driver, "rpg net")

    count = count + 1

# Gets the amount of life potions in the players inv
def get_life_potions(driver):
    send_message(driver, "rpg i")
    inv_elements = driver.find_elements_by_xpath("//img[@aria-label=':lifepotion:']")
    inv_element = inv_elements[len(inv_elements)-1]
    inv_txt = inv_element.find_element_by_xpath("./..").text

    return re.search("life potion: (.*)", inv_txt).group(1)

# checks if need to buy a life potion
def buy_life_potion(driver):
    if int(get_life_potions(driver)) < 10:
        send_message(driver, "rpg buy life potion")

# Gets the players health as an int
def get_stats(driver):
    send_message(driver, "rpg p")
    
    stats_elements = driver.find_elements_by_xpath("//img[@aria-label=':heart:']")
    stats_element = stats_elements[len(stats_elements)-1]
    stats_txt = stats_element.find_element_by_xpath("./..").text

    coin_elements = driver.find_elements_by_xpath("//img[@aria-label=':coin:']")
    coin_element = coin_elements[len(coin_elements)-1]
    coin_txt = coin_element.find_element_by_xpath("./..").text

    stats = {
        '$' : re.search("Coins: (.*)", coin_txt).group(1),
        'pots': get_life_potions(driver),
        'AT': re.search("AT: (.*)\n", stats_txt).group(1),
        'DE': re.search("DEF: (.*)\n", stats_txt).group(1),
        'HP': re.search("LIFE: (.*)", stats_txt).group(1)
    }
    
    print(stats)
    return stats

# Convert a string like "4/5" to 0.8
def get_hp_as_pct(stats):
    num = float(re.search("(.*)/", stats['HP']).group(1))
    den = float(re.search("/(.*)", stats['HP']).group(1))
    return num / den

# Checks if a captcha has been thrown
def detect_captcha(driver):
    # keep track of minimal
    try:
        img_elements = driver.find_elements_by_xpath("//a[@href='*.epic_guard.png']")
        print(img_elements)
        img_element = img_elements[len(img_elements)-1]
        img_url = img_element.get_attribute('href') 
        filename = "./defeated_captchas/defeated.png"

        user_agent = 'Mozilla/5.0 (iPhone; CPU iPhone OS 5_0 like Mac OS X) AppleWebKit/534.46'
        img_url = "https://cdn.discordapp.com/attachments/623235554762424340/701268445764780112/epic_guard.png"

        response = requests.get(img_url, stream=True, headers={'User-Agent': user_agent})
        with open(filename, 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)
        del response

        captcha = translate_img(filename)
        print(f"Captcha defeated: {captcha}")
        send_message(driver, captcha)
    except:
        print("No captcha, keep playin brother")


# converts an epic_guard captcha to a string
def translate_img(img_name):
    img = cv2.imread(img_name, 0)
    img_i = cv2.bitwise_not(img)
    # cv2.imshow("input", img_i)
    # cv2.waitKey(0)
    txt = pytesseract.image_to_string(img_i)
    cleaned = txt.replace("\"", "")
    print(f"Capthcha: {cleaned}")
    return cleaned

# 5 minute cd
def five_cycle(driver, gather_count, focus="even"):
    gather_1(driver, gather_count, focus="wood")
    for i in range(5):
        hunt(driver)
        time.sleep(65)
        hunt(driver)
        time.sleep(65)
        hunt(driver)
        time.sleep(65)
        hunt(driver)
        time.sleep(65)
        hunt(driver)
        time.sleep(65)
    send_message(driver, random.choice(QUIPS))
    

# hunts every minute, gathers every 5, and advs every 60
def sixty_cycle(driver, gather_count, focus="even"):
    for i in range(12):
        print(f"On cycle {i+1}/12")
        five_cycle(driver, gather_count, focus=focus)
    adventure(driver)

