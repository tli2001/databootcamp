import time
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
import requests
from pprint import pprint

def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()
    mars_data = {}

    # data sources across 5 websites
    url1 = 'https://mars.nasa.gov/news/'
    url2 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    url3 = 'https://twitter.com/marswxreport?lang=en'
    url4 = 'http://space-facts.com/mars/'
    url5 = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    # open and parse each url
    browser.visit(url1)
    time.sleep(1)
    html1 = browser.html
    soup1 = BeautifulSoup(html1, "html.parser")
   
    browser.visit(url2)
    time.sleep(1)
    html2 = browser.html
    soup2 = BeautifulSoup(html2, "html.parser")

    browser.visit(url3)
    time.sleep(1)
    html3 = browser.html
    soup3 = BeautifulSoup(html3, "html.parser")

    browser.visit(url4)
    time.sleep(1)
    html4 = browser.html
    soup4 = BeautifulSoup(html4, "html.parser")

    browser.visit(url5)
    time.sleep(1)
    html5 = browser.html
    soup5 = BeautifulSoup(html5, "html.parser")

    # scrape and store data from each site
    mars_data['news_title'] = soup1.find("div", class_="content_title").get_text()
    mars_data['news_para'] = soup1.find("div", class_="rollover_description_inner").get_text()
    
    slide = soup2.find('li', class_='slide')
    pic_url = slide.find('a', class_='fancybox')
    featured_image_base = 'https://www.jpl.nasa.gov'
    featured_image_url = featured_image_base + pic_url['data-fancybox-href']
    
    mars_data['featured_title'] = pic_url['data-title']
    mars_data['featured_image'] = featured_image_url

    mars_weather = soup3.find('div', class_='js-tweet-text-container').get_text()
    mars_data['weather'] = mars_weather.replace('\n',"")

    tables = pd.read_html(url4)
    mars_df = pd.DataFrame(tables[0])
    mars_df.columns = ['Measurement',"Value"]
    mars_df.set_index('Measurement', inplace=True)
    marsfactsdict = mars_df.to_dict()
    mars_data['facts'] = marsfactsdict

    results = soup5.find_all('div', class_='item')
    img_dl_base = 'https://astrogeology.usgs.gov'
    # list and dictionary set up to store hemisphere titles and image urls
    hemilist = []
    hemidict = {}

    for result in results:
        try:
            # Identify and return hemisphere title
            hemi_title = result.find("h3").text
            # Identify and return image of hemisphere [this link goes to the image dl page]
            img_dl_url = result.a['href']
            # construct link to download the hemisphere image
            url = img_dl_base + img_dl_url
            # use constructed link to scrape hemisphere image
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'lxml')
            result = soup.find("div", class_="downloads")
            # save hemisphere image url
            hemi_url = result.a['href']
        except Exception as e:
            print(e)
        # Python Dictionary of hemisphere title and image url
        hemidict = {
            'title': hemi_title,
            'img_url': hemi_url,
        }
        # Append hemisphere dictionary to list 
        hemilist.append(hemidict)
    mars_data['hemi'] = hemilist    

    return mars_data

# test = scrape()
# pprint(test)