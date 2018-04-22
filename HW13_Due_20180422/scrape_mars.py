import time
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver


def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()
    mars_data = {}

    url1 = 'https://mars.nasa.gov/news/'
#    url2 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
#    url3 = 'https://twitter.com/marswxreport?lang=en'
#    url4 = 'http://space-facts.com/mars/'
#    url5 = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url1)
    time.sleep(1)

    html1 = browser.html
    soup1 = BeautifulSoup(html1, "html.parser")

#    listings["headline"] = soup.find("a", class_="result-title").get_text()
#    listings["price"] = soup.find("span", class_="result-price").get_text()
#    listings["hood"] = soup.find("span", class_="result-hood").get_text()
    mars_data['news_title'] = soup1.find("div", class_="content_title").get_text()
    mars_data['news_para'] = soup1.find("div", class_="rollover_description_inner").get_text()
    
    return mars_data

test = scrape()
print(test)