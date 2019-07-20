# Import Dependecies
from bs4 import BeautifulSoup
from splinter import Browser
import pandas as pd
import requests
import time

# Initialize browser


def init_browser():
    # Replace the path with your actual path to the chromedriver

    # Windows Users
    # executable_path = {'C:/users/anup/Homework_12webScrapping/WebScrappingHomework/chromedriver.exe'}
    # return Browser('chrome', **executable_path, headless=False)
    exec_path = {'executable_path': './chromedriver.exe'}
    return Browser('chrome', headless=False, **exec_path)


# Create Mission to Mars global dictionary that can be imported into Mongo
mars_info = {}
init_browser()

# NASA MARS NEWS


def scrape_mars_news():

    # Initialize browser
    browser = init_browser()

    # Visit Nasa news url through splinter module
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    # HTML Object
    html = browser.html

    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html, 'html.parser')

    # Retrieve the latest element that contains news title and news_paragraph
    news_title = soup.find('div', class_='content_title').find('a').text
    news_p = soup.find('div', class_='article_teaser_body').text

    # Dictionary entry from MARS NEWS
    mars_info['news_title'] = news_title
    mars_info['news_paragraph'] = news_p

    return mars_info


# FEATURED IMAGE

def scrape_mars_image():

    # Initialize browser

    browser = init_browser()

    image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"

    browser.visit(image_url)

    # navigate to link

    browser.click_link_by_partial_text('FULL IMAGE')

    time.sleep(2)

    browser.click_link_by_partial_text('more info')

    time.sleep(2)

    # get html code once at page

    image_html = browser.html

    # parse

    soup = BeautifulSoup(image_html, "html.parser")

    # find path and make full path
    image_path = soup.find('figure', class_='lede').a['href']

    featured_image_url = "https://www.jpl.nasa.gov" + image_path

    mars_info['featured_image_url'] = featured_image_url

    # print(featured_image_url)

    return mars_info

# Mars Weather


def scrape_mars_weather():

    # Initialize browser
    browser = init_browser()

    # browser.is_element_present_by_css("div", wait_time=1)

    # Visit Mars Weather Twitter through splinter module
    weather_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(weather_url)

    # HTML Object
    html_weather = browser.html

    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html_weather, 'html.parser')

    # Find all elements that contain tweets
    latest_tweets = soup.find_all('div', class_='js-tweet-text-container')

    # Retrieve all elements that contain news title in the specified range
    # Look for entries that display weather related words to exclude non weather related tweets
    for tweet in latest_tweets:
        weather_tweet = tweet.find('p').text
        if 'Sol' and 'pressure' in weather_tweet:
            print(weather_tweet)
            break
        else:
            pass

    # Dictionary entry from WEATHER TWEET
    mars_info['weather_tweet'] = weather_tweet

    return mars_info


# Mars Facts

def scrape_mars_facts():

    browser = init_browser()

    # Visit Mars facts url
    facts_url = 'http://space-facts.com/mars/'

    # Use Panda's `read_html` to parse the url
    mars_facts = pd.read_html(facts_url)

    # Find the mars facts DataFrame in the list of DataFrames as assign it to `mars_df`
    mars_df = mars_facts[0]

    # Assign the columns `['Description', 'Value']`
    mars_df.columns = ['Mars-Earth Comparison', 'Mars', 'Earth']

    # Set the index to the `Description` column without row indexing
    mars_df.set_index('Mars-Earth Comparison', inplace=True)

    # Save html code to folder Assets
    data = mars_df.to_html()

    # Dictionary entry from MARS FACTS
    mars_info['mars_facts'] = data


# MARS HEMISPHERES

def scrape_mars_hemispheres():
    # Initialize browser
    browser = init_browser()

    # Visit hemispheres website through splinter module
    hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemispheres_url)

    # HTML Object
    html_hemispheres = browser.html

    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html_hemispheres, 'html.parser')

    # Retreive all items that contain mars hemispheres information
    items = soup.find_all('div', class_='item')

    # Create empty list for hemisphere urls
    hiu = []

    # Store the main_ul
    hemispheres_main_url = 'https://astrogeology.usgs.gov'

    # Loop through the items previously stored
    for i in items:
        # Store title
        title = i.find('h3').text

        # Store link that leads to full image website
        partial_img_url = i.find(
            'a', class_='itemLink product-item')['href']

        # Visit the link that contains the full image website
        browser.visit(hemispheres_main_url + partial_img_url)

        # HTML Object of individual hemisphere information website
        partial_img_html = browser.html

        # Parse HTML with Beautiful Soup for every individual hemisphere information website
        soup = BeautifulSoup(partial_img_html, 'html.parser')

        # Retrieve full image source
        img_url = hemispheres_main_url + \
            soup.find('img', class_='wide-image')['src']

        # Append the retreived information into a list of dictionaries
        hiu.append({"title": title, "img_url": img_url})

    mars_info['hiu'] = hiu

    return mars_info