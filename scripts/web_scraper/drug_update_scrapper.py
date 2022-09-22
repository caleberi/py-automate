from csv import DictWriter
import pandas as pd
from datetime import datetime
from typing import Callable, List, Optional
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.webdriver import WebDriver, Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By

from os import path, getcwd

# set up selenium for chrome

PASSWORD = "Debby1"
EMAIL = "siloampharmacy_abeokuta@yahoo.com"


def file_exist(pth: str):
    return True if path.exists(pth) and path.isfile(pth) else False


def create_web_service(srv_args: Optional[List[str]]):
    """
    Creates a service instance
    Params:
        srv_args - list of args pass to chrome driver
    """
    pth = path.abspath(path.join(getcwd(), "../../chrome"))
    log_pth = path.abspath(path.join(getcwd(), "./logs/service.txt"))
    if not file_exist(log_pth):
        try:
            open(log_pth, O_CREAT)
        except Exception as err:
            print(f"error occurred while creating {log_pth}", err)
    if srv_args:
        return Service(pth, service_args=srv_args)
    return Service(pth, log_path=log_pth)


def create_web_options(headless: Optional[bool]):
    opts = webdriver.ChromeOptions()
    opts.add_argument("--disable-infobars")
    opts.add_argument("--disable-extensions")
    opts.add_argument("--start-maximized")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-gpu")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--incognito")
    opts.add_argument("--disable-xss-auditor")
    opts.add_argument("--disable-web-security")
    opts.add_argument("--allow-running-insecure-content")
    opts.add_argument("--disable-setuid-sandbox")
    opts.add_argument("--disable-webgl")
    opts.add_argument("--disable-popup-blocking")
    # pass the argument 1 to allow and 2 to block
    opts.add_experimental_option(
        "prefs",
        {
            "profile.default_content_setting_values.media_stream_mic": 2,
            "profile.default_content_setting_values.media_stream_camera": 2,
            "profile.default_content_setting_values.geolocation": 2,
            "profile.default_content_setting_values.notifications": 2,
        },
    )
    opts.add_experimental_option("excludeSwitches", ["enable-automation"])
    opts.add_argument("disable-blink-features=AutomationControlled")
    if headless:
        opts.add_argument("--headless")
    return opts


def create_web_driver(srv: Optional[Service], opts: Optional[Options]) -> WebDriver:
    if not srv:
        srv = create_web_service(None)
    if not opts:
        opts = create_web_options(True)
    return WebDriver(service=srv, options=opts)


def process_website(drv: WebDriver, fn: Callable[[WebDriver], WebDriver]):
    drv = good_all_page_login(drv)

    drv.implicitly_wait(10)

    elements = drv.find_elements(By.CSS_SELECTOR, "#wrp > tr")

    drv.implicitly_wait(10)

    csv_data = []

    for idx in range(len(elements) - 1):
        product_title = drv.find_element(
            By.XPATH,
            f"//*[@id='wrp']/tr[{idx+1}]/td/form/div/div[1]/div/div[1]/h4",
        ).text

        data = drv.find_element(
            By.XPATH,
            f"//*[@id='wrp']/tr[{idx+1}]/td/form/div/div[1]/div/div[1]/h5",
        ).text.strip()

        batch_id, price_per_unit, qty = tuple(data.split("|"))
        csv_data.append(
            (
                product_title,
                batch_id.strip(),
                price_per_unit.strip()[7:],
                int(qty.strip()[5:]) + 1,
            )
        )

    drv.implicitly_wait(5)

    now = datetime.now()

    file_name = now.strftime("%Y-%m-%d-%H:%M:%S") + ".csv"

    out_path = path.abspath(path.join(getcwd(), f"./output/{file_name}"))

    fieldnames = ["product_title", "batch_id", "price_per_unit", "qty"]

    with open(out_path, "w", newline="", encoding="utf-8") as csv_file:

        writer = DictWriter(csv_file, fieldnames=fieldnames)

        writer.writeheader()

        for dt in csv_data:
            print(dt)
            product_title, batch_id, price_per_unit, qty = dt
            writer.writerow(
                {
                    "product_title": product_title,
                    "batch_id": batch_id,
                    "price_per_unit": price_per_unit,
                    "qty": str(qty),
                }
            )

    drv.implicitly_wait(5)
    drv.close()

    return out_path


def good_all_page_login(drv: WebDriver) -> WebDriver:
    drv.implicitly_wait(5)
    drv.find_element(By.XPATH, "//*[@id='Email']").send_keys(EMAIL)
    drv.find_element(By.XPATH, "//*[@id='Password']").send_keys(PASSWORD)
    drv.find_element(
        By.XPATH, "//*[@id='customer_login']/div[3]/div[1]/div/button"
    ).submit()
    return drv


def convert_csv_to_xls(csv_path: str) -> str:
    out_path = csv_path.split(".")[0] + ".xlsx"
    df_new = pd.read_csv(csv_path)
    GFG = pd.ExcelWriter(out_path)
    df_new.to_excel(GFG, index=True)
    GFG.save()
    return out_path

def compare_docs_and_highlight(updated_wholesales_doc_path:str,business_doc_path:str):
    # read the updated_wholesales_doc against the business_doc and perform highlighting
    wdoc = pd.read_excel(updated_wholesales_doc_path)
    bdoc = pd.read_excel(business_doc_path)

    # for each df in data-frame for bdoc 
    # extract the name for the column and get all df for the wdoc 
    # and compare the likely hood of that matching the  wdoc[i] dataframe entry
    
    

    # new price at current time  
    pass

def browse(url: str, srv: Optional[Service], opts: Optional[Options]):
    try:
        drv: WebDriver = create_web_driver(srv=srv, opts=opts)
        drv.get(url)
        # wait for page load
        WebDriverWait(drv, 5).until(
            ec.all_of(
                ec.presence_of_element_located((By.XPATH, "//*[@id='Email']")),
                ec.presence_of_element_located((By.XPATH, "//*[@id='Password']")),
            )
        )
        business_doc_path = "./business.xlsx"
        csv_path = process_website(drv, process_website)
        updated_wholesales_doc_path = convert_csv_to_xls(csv_path)
        compare_docs_and_highlight(
            updated_wholesales_doc_path=updated_wholesales_doc_path,
            business_doc_path=business_doc_path
        )

    except Exception as e:
        print(e)


if __name__ == "__main__":
    browse("https://goodallpharmacy.com/login", None, None)
