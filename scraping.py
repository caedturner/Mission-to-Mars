
# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt

# Initialize, browser, create data dictionary, end webdriver and return scraped data.
def scrape_all():
    # initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', ** executable_path, headless=True)

    # set news_title and news_paragraph variables
    news_title, news_paragraph = mars_news(browser)
    # run all scraping finctions and store results in a dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now()
    }
    # Stop the webdriver and return data
    browser.quit()
    return data

def mars_news(browser):

    # Visit the NASA news site
    url = 'https://redplanetscience.com'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Convert the browser html to a sopu object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')
    #slide_elem = news_soup.select_one('div.list_text')

    #slide_elem.find('div', class_='content_title')

    # Use the parent element to find the firsdt 'a' tag and save it as 'news_title'
    #news_title = slide_elem.find('div', class_='content_title').get_text()


    # Use the parent element to find the paragraph text
    #news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
    
    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')
        # Use the parent element to find the first 'a' tag and save it as 'news title'
        news_title = slide_elem.find('div', class_=content_title).get_text()
        # Use the parent element to find the paragraph text.
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

    except AttributeError:
        return None, None

    return news_title, news_p



# Begin Image Scrape
def featured_image(browser):
    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting HTML with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Find the relative image url
    #img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
    

    #img_url = f'https://spaceimages-mars.com/{img_url_rel}'
    
    # Add a Try/Except for error handling
    try:
        # find the relative image
        img_url_rel = img_soup.find('img', class_='fancybox-image')

    except AttributeError:
        return None
    
    return img_url

# Scrape the Facts Table
def mars_facts():
    try:
        # Use 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
    except BaseException():
        return None
    # Assign Columns and set index of DataFrame
    df.columns=['description', 'Mars', 'Earth']
    df.set_index('description', inplace=True)

    # Convert DataFrame to HTML format, add bootstrap
    return df.to_html()
    
    
    
if __name__ == "__main__":
    #if runnung as script, print scraped data
    print(scrape_all())

