import json
import numpy as np
import pandas as pd
import os
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import unicodedata
import matplotlib.pyplot as plt
import time
from selenium import webdriver
from passwords import *

def find_and_send(contacts):

    for contact in contacts:
        wordcloud_dir = create_wordcloud(contact)

        search_box = driver.find_element_by_xpath('/html/body/div[1]/div/div/div[1]/div[2]/div[3]/div/div[1]/div/div/div[1]/span[1]/label/input')
        search_box.click()                                                                                                 
        search_box.send_keys(contact)

        time.sleep(3)

        person = driver.find_element_by_xpath('/html/body/div[1]/div/div/div[1]/div[2]/div[3]/div/div[1]/div/div/div[1]/span[1]/div/div/div[2]/ul/li/a/div/div[2]/div/div')
        person.click()

        time.sleep(5)

        input_box = driver.find_element_by_xpath('/html/body/div[1]/div/div/div[2]/span/div[2]/div[2]/div[2]/div/div[4]/div/div/div[1]/div/div[2]/div')
        input_box.click()

        input_box.send_keys('Hello! Look at our wordcloud! ')
        # send_btn = driver.find_element_by_xpath('/html/body/div[1]/div/div/div[2]/span/div[2]/div[2]/div[2]/div[2]/a')
        # send_btn.click()

        attach_file = driver.find_element_by_xpath('/html/body/div[1]/div/div/div[2]/span/div[2]/div[2]/div[2]/div/div[3]/div[2]/form/div/span/input')  
        attach_file.send_keys(wordcloud_dir)

        send_btn = driver.find_element_by_xpath('/html/body/div[1]/div/div/div[2]/span/div[2]/div[2]/div[2]/div[2]/a')
        send_btn.click()

        time.sleep(5)

def twofactorauth():

    continue_btn = driver.find_element_by_xpath('//*[@id="XMessengerDotComLoginViewPlaceholder"]/div/div[1]/div/a')
    continue_btn.click()
    
    # time.sleep(15)
    temp = "p"
    while temp:
        print("Press enter if you are ready with 2FA")
        temp = input()

    # press enter to continue..

    continue1 = driver.find_element_by_xpath('//*[@id="XMessengerDotComLoginViewPlaceholder"]/div/div[1]/div/a')
    continue1.click()

    continue2 = driver.find_element_by_id('checkpointSubmitButton')
    continue2.click()

    this_was_me = driver.find_element_by_id('checkpointSubmitButton')
    this_was_me.click()

    dont_save = driver.find_element_by_id('u_0_3')
    dont_save.click()

    continue3 = driver.find_element_by_id('checkpointSubmitButton')
    continue3.click()

def create_wordcloud(name):

    name1 = name.lower().replace(" ", "") + ".json"


    working_dir = os.getcwd()
    file_location = find(name1, working_dir)

    with open(file_location) as file:
        chat_history = json.load(file)

    messages = pd.DataFrame(chat_history['messages'])
    text = " ".join(str(x) for x in messages.content if not isNaN(x))
    normalized_text = normalize(text)

    wordcloud = WordCloud(stopwords=STOPWORDS, background_color="white").generate(normalized_text)
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    # file_name = name.replace(" ", "_")
    wordcloud_dir = working_dir + "\\wordclouds\\" + name.replace(" ", "_") + ".png"
    wordcloud.to_file(wordcloud_dir)
    
    return wordcloud_dir

def find(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)

def isNaN(string):
    return string != string

def normalize_char(c):
    try:
        cname = unicodedata.name(c)
        cname = cname[:cname.index(' WITH')]
        return unicodedata.lookup(cname)
    except (ValueError, KeyError):
        return c

def normalize(s):
    return ''.join(normalize_char(c) for c in s)

try:
    driver = webdriver.Chrome()
except Exception:
    path = input("Please input the path the the chromedriver executable: ")

contacts = []
while True:
    usr_input = input("Enter your friend(s) name: ").strip().title()
    if usr_input == "":
        break
    contacts.append(usr_input)

# driver = webdriver.Chrome(r"\Users\calin\Downloads\chromedriver.exe")

driver = webdriver.Chrome(path)
driver.maximize_window()
driver.get('https://www.messenger.com')
time.sleep(5)

email_input = driver.find_element_by_id("email")
password_input = driver.find_element_by_id("pass")
login_button = driver.find_element_by_id("loginbutton")

email_input.send_keys(email)
password_input.send_keys(password)
login_button.click()

try:
    find_and_send(contacts)
    print("Trying.....")
except Exception:
    print("Error. I have to use 2FA")
    twofactorauth()
    find_and_send(contacts)