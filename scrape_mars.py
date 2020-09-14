from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
import pandas as pd
import time

def init_browser():
    # Setting up windows browser with chromedriver
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    return browser

def scrape():
    browser = init_browser()
    mars_data = {}
    
###################################
#Mars Headlines
###################################

    # A blank list to hold the headlines and descriptions
    news_titles = []
    news_p = []

    #URL to be scraped
    news_url = 'https://mars.nasa.gov/news/'
    browser.visit(news_url)
    time.sleep(1)

    html = browser.html
    soup = bs(html, 'lxml')

    results = soup.find_all('div', class_='slide')
    
    # Loop over div elements
    for result in results:
        
        news_title = result.find('div', class_='content_title').a.text
        news_titles.append(news_title)
        
        description = result.find('div', class_='rollover_description_inner').text
        news_p.append(description)

###################################
#Mars Featured Image
###################################
    
    # Visit URL for featured space image
    image_url = "https://www.jpl.nasa.gov/spaceimages/"
    base_url = "https://www.jpl.nasa.gov"
    browser.visit(image_url)
    time.sleep(1)

    # Parse HTML with Beautiful Soup
    html = browser.html
    image_soup = bs(html, 'lxml')

    # Scrape the URL
    feat_img = image_soup.find('a', class_='button fancybox')['data-fancybox-href']

    #Compose full image URL
    featured_image_url = base_url + feat_img
    
###################################
#Mars Facts
###################################

    facts_url = "https://space-facts.com/mars/"
    browser.visit(facts_url)
    time.sleep(1)

    response = requests.get(facts_url)
    soup = bs(response.text, 'lxml')

    #put data in a pandas dataframe
    table = pd.read_html(facts_url)
    mars_facts = table[0]
    mars_facts.columns = ['Attribute', 'Information']
    
    #turn into HTML table string
    mars_facts_html = mars_facts.to_html(table_id="mars_facts",justify='left',index=False).replace("\n", "")

###################################
#Mars Hemispheres
###################################

    hem_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    base_url = 'https://astrogeology.usgs.gov'
    browser.visit(hem_url)
    time.sleep(1)
    
    image_titles = []
    image_links = []

    # HTML object
    hem_html = browser.html
    
    # Parse HTML with Beautiful Soup
    soup = bs(hem_html, 'lxml')
    
    # Retrieve all elements that contain hemisphere photo info
    results = soup.find_all('div', class_='description')
    
    for i in results:
        # Use Beautiful Soup's find() method to navigate and retrieve attributes
        image_title = i.a.find('h3').text
        image_link = i.find('a')['href']
        target_link = base_url + image_link

        image_titles.append(image_title)
        image_links.append(target_link)

    # Hemisphere 1
    browser.visit(image_links[0])
    time.sleep(1)
    html = browser.html
    soup = bs(html, 'lxml')
    results = soup.find_all('div', class_='content')

    for o in results:
        full_im1_link = browser.links.find_by_partial_text('Sample')['href']
    
    # Hemisphere 2
    browser.visit(image_links[1])
    time.sleep(1)
    html = browser.html
    soup = bs(html, 'lxml')
    results = soup.find_all('div', class_='content')

    for o in results:
        full_im2_link = browser.links.find_by_partial_text('Sample')['href']

    # Hemisphere 3
    browser.visit(image_links[2])
    time.sleep(1)
    html = browser.html
    soup = bs(html, 'lxml')
    results = soup.find_all('div', class_='content')

    for o in results:
        full_im3_link = browser.links.find_by_partial_text('Sample')['href']

    # Hemisphere 4
    browser.visit(image_links[3])
    time.sleep(1)
    html = browser.html
    soup = bs(html, 'lxml')
    results = soup.find_all('div', class_='content')

    for o in results:
        full_im4_link = browser.links.find_by_partial_text('Sample')['href']

###################################
#Storing everything in a dictionary
###################################
    mars_data = {
       "news_title": news_titles,
       "news_p": news_p,
       "featured_image": featured_image_url,
       "mars_specs": mars_facts_html,
       "mars_hem_names": image_titles,
       "mars_hem_links": [full_im1_link, full_im2_link, full_im3_link, full_im4_link]
    }

    return mars_data

if __name__ == "__main__":
    scrape()