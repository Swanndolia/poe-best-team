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

BUCKET = "scraper_github"


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
    driver.get(arg)
    scrap(driver, arg, BUCKET)


def scrap(driver, url, BUCKET):
    last_commit = driver.find_element_by_tag_name(
        "relative-time").get_attribute("outerHTML")
    start = last_commit.find("datetime=\"") + 10
    end = last_commit.find("T")
    popularity = driver.find_elements_by_class_name(
        "pagehead-actions.flex-shrink-0.d-none.d-md-inline")
    borders = driver.find_elements_by_class_name("BorderGrid-cell")
    data = {}
    data["last_commit"] = (last_commit[start:end])
    for element in popularity:
        if not "popularity" in data:
            data["popularity"] = []
        data["popularity"].append(element.text)
    for element in borders:
        if not "infos" in data:
            data["infos"] = []
        data["infos"].append(element.text)
    print(data)

    blob_path = "scrap_git_" + arg
    storage_client = storage.Client()
    if storage_client.bucket(BUCKET).exists():
        mybucket = storage_client.get_bucket(BUCKET)
    else:
        mybucket = storage_client.create_bucket(BUCKET)
    myblob = mybucket.blob(blob_path)
    myblob.upload_from_string(data)
    print(myblob)
    sys.exit()


if(__name__ == "__main__"):
    for arg in sys.argv:
        if(arg != "__main__.py"):
            print(arg)
            try:
                thread = Thread(target=run_thread, args=(arg,))
                thread.start()
            except:
                print("Error: unable to start thread")