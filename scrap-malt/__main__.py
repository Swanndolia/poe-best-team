import json
import time
import sys
import os
import socket
from threading import Thread
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
from google.cloud import storage

BUCKET = "scraper_malt"

def normalize_text(text):
    text = text.strip().replace("é", "e").replace("è", "e").replace("à", "a").replace("ê", "e").replace("ù", "u")
    return text.lower()

def run_thread(arg):
    options = Options()
    ua = UserAgent(verify_ssl=False)
    userAgent = ua.chrome
    options.add_argument(f'user-agent={userAgent}')
    options.add_argument("--disable-extensions")
    options.add_argument('--no-sandbox')
    options.add_argument("--headless")
    options.add_argument("--start-maximized")
    options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(options=options)
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
                Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
                })
            """
    })
    driver.maximize_window()
    url = "https://www.malt.fr/s?q=" + arg
    driver.get(url)
    with open('cookies.json', 'r', newline='') as inputdata:
        cookies = json.load(inputdata)
    for cookie in cookies:
        cookie.pop('sameSite')
        driver.add_cookie(cookie)
    time.sleep(3)
    driver.get(url)
    scrap(driver, arg, BUCKET)


def scrap(driver, techno, BUCKET):
    time.sleep(2)
    elements = driver.find_elements_by_class_name(
        "profile-card.freelance-linkable")
    for element in elements:
        time.sleep(1)
        comps = element.find_elements_by_css_selector("li.m-tag.m-tag_secondary.m-tag_small span")
        data = {}
        data["name"] = normalize_text(element.find_element_by_class_name(
            "profile-card-header__full-name").text)
        data["prix"] = element.find_element_by_css_selector("p.js-trigger.c-tooltip_target.profile-card-price__rate strong").text.replace("€", "")
        data["tech"] = [normalize_text(comp.get_attribute("textContent")) for comp in comps]
        data["metier"] = normalize_text(element.find_element_by_class_name("profile-card-body__headline.profile-card-body__headline__capitalized").text)
        data_json = json.dumps(data)
        print(data_json)
        # blob_path = name.replace(" ", "_") + "_" + techno #replace with hash
        # storage_client = storage.Client()
        # if storage_client.bucket(BUCKET).exists():
        #     mybucket = storage_client.get_bucket(BUCKET)
        # else:
        #     mybucket = storage_client.create_bucket(BUCKET)
        # myblob = mybucket.blob(blob_path)
        # myblob.upload_from_string(data_json)
    try:
        next_page = driver.find_element_by_class_name("c-pagination__next")
        time.sleep(1)
        ActionChains(driver).move_to_element(
            next_page).click(next_page).perform()
        scrap(driver, techno, BUCKET)
    except:
        sys.exit()


if(__name__ == "__main__"):
    for arg in sys.argv:
        if(arg != "__main__.py"):
            try:
                thread = Thread(target=run_thread, args=(arg,))
                thread.start()
            except:
                print("Error: unable to start thread")
    thread = Thread(target=run_thread, args=("python",))
    thread.start()
