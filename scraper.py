# Selenium for web scraping
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import pandas as pd
import time

# send key for zoom functionality perhaps
from selenium.webdriver.common.keys import Keys

# my files
import tests
import funcs as myfunc


def scraper():
    """
    Takes no arguments.

    Web scrapes weekly deals on hemköp.se
    :return: returns a dataframe
    """

    # open firefox
    driver = webdriver.Firefox()
    driver.maximize_window()
    # navigate to page
    driver.get("https://www.hemkop.se/veckans-erbjudanden")
    time.sleep(3)

    # accept cookies button click
    WebDriverWait(driver, 2)  # wait 3 sec
    element = driver.find_element(By.XPATH, "//*[@id='onetrust-accept-btn-handler']")
    element.click()
    WebDriverWait(driver, 2)

    # todo:         FUTURE IMPLEMENTATION: zoom functionality for faster scraping
    # win = driver.find_element(By.TAG_NAME, "body")
    # win.send_keys(Keys.CONTROL, "-")#zoom to 120%
    # # driver.execute_script("document.body.style.MozTransform='scale(0.3)'")

    # Scrolling
    time.sleep(3)
    previous_height = driver.execute_script("return document.body.scrollHeight")
    # scroll the infinity scroll
    while True:
        # set previous height to current height
        previous_height = driver.execute_script("return document.body.scrollHeight")
        # scroll to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        # set new height to current height
        new_height = driver.execute_script("return document.body.scrollHeight")
        # if new height and current height is the same, it means we reached the bottom of the page
        if new_height == previous_height:
            break

    # Scrape part
    # like the container method, we define content as the whole block containing all the foods
    content = driver.find_element(By.CSS_SELECTOR,
                                  "div[class*='ax-product-grid content-grid ifcontent']")

    item = content.find_elements(By.CSS_SELECTOR,
                                 "div[class*='product-puff selenium--product-puff layout-align-start-center layout-column']")

    # todo:         FUTURE IMPLEMENTATION: extract image

    # initializing lists
    name_lst = []
    price_lst = []
    original_price_lst = []
    original_jmf_lst = []
    discounted_jmf_lst = []
    brand_lst = []
    weight_lst = []

    # scraping the data
    for element in item:
        myfunc.get_data(name_lst, "div[class*='product-puff-name']>a[class*='product-puff-image']", element)
        myfunc.get_data(price_lst, "div[class*='product-price-label-price']>span[class*='selenium-puff-price']",
                        element)
        myfunc.get_data(original_price_lst, "span.product-ordinary-price", element)
        myfunc.get_data(original_jmf_lst, "span.product-compare-price", element)
        myfunc.get_data(discounted_jmf_lst, "span.product-price-label-promotion-info", element)
        myfunc.get_data(brand_lst, "div[class*='product-puff-manufacturer']>span:nth-child(1)", element)
        myfunc.get_data(weight_lst, "div[class*='product-puff-manufacturer']>span:nth-child(3)", element)

    # checking the lengths of the lists to spot inconsistencies
    tests.len_test(name_lst, price_lst, brand_lst, weight_lst, original_price_lst, original_jmf_lst, discounted_jmf_lst)

    # create a dataframe with gathered data
    df = pd.DataFrame(
        {'Name': name_lst,
         'Price': price_lst,
         'Original Price': original_price_lst,
         'Original compare price': original_jmf_lst,
         'Discounted compare price': discounted_jmf_lst,
         'Brand': brand_lst,
         'Weight': weight_lst
         })

    return df
