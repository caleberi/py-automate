from os import path, getcwd
import time 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from time import gmtime, strftime


service = Service(path.join(getcwd(),"../../chrome"))


def create_driver():
    opts =  webdriver.ChromeOptions()
    opts.add_argument("disable-infobars")
    opts.add_argument("start-maximized")
    opts.add_argument("disable-dev-shm-usage")
    opts.add_argument("no-sandbox")
    opts.add_experimental_option("excludeSwitches",["enable-automation"])
    opts.add_argument("disable-blink-features=AutomationControlled")

    driver = webdriver.Chrome(service=service,options=opts)
    driver.get("http://automated.pythonanywhere.com")
    return driver

def clean_text(text:str):
    """Extract only the temperature from text body"""
    output = text.split(": ")
    return output[-1]

def main():
    drv =  create_driver()
    time.sleep(8)
    drv.find_element(By.XPATH,"//*[@id=\"basicExampleNav\"]/div/a").click()
    time.sleep(2)
    drv.find_element(By.ID,"id_username").send_keys("automated")
    time.sleep(2)
    drv.find_element(By.ID,"id_password").send_keys("automatedautomated" + Keys.ENTER)
    time.sleep(1)
    drv.find_element(By.XPATH,"/html/body/nav/div/a").click()
    time.sleep(5)
    text = drv.find_element(By.XPATH,"/html/body/div[1]/div/h1[2]").text
    element = float(clean_text(text))
    return f"Current Value : {element}"

def automate():
    cnt = 0
    while cnt < 10:
        file_name = strftime("%Y- %m - %d {%H:%M:%S}",gmtime())+'.txt'
        with open(file=file_name,mode='w') as f:
            f.write(main())
            time.sleep(3)
            f.close()
        cnt+=1

automate()

