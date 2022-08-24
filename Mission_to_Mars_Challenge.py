#!/usr/bin/env python
# coding: utf-8

# In[12]:


# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


# In[13]:


executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', ** executable_path, headless=False)


# In[14]:


# Visit the NASA news site
url = 'https://redplanetscience.com'
browser.visit(url)
# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)


# In[15]:


html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')


# In[16]:


slide_elem.find('div', class_='content_title')


# In[17]:


# Use the parent element to find the firsdt 'a' tag and save it as 'news_title'
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title


# In[18]:


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# ### Begin Image Scrape

# In[19]:


# VIsit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)


# In[20]:


# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# In[21]:


# Parse the resulting HTML with soup
html = browser.html
img_soup = soup(html, 'html.parser')


# In[22]:


# Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel


# In[23]:


img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


# ### Scrape the Facts Table

# In[24]:


df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.columns=['description', 'Mars', 'Earth']
df.set_index('description', inplace=True)
df


# In[25]:


df.to_html()


# In[36]:


browser.quit()


# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# ### Hemispheres

# In[70]:


# 1. Use browser to visit the URL 
# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


# In[86]:


# Reinstate Browser
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', ** executable_path, headless=False)


# In[87]:


url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

browser.visit(url)


# In[88]:


# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.
links = browser.find_by_css('a.product-item h3')

# Loop to click hemisphere link - find full resolution image - 
#retrieve full resolution image URL string and title of image - 
# go back and get the next Hemisphere
for i in range(len(links)):
    # Create a dictionarty to hold data scraped
    hemisphere = {}
    # Find and click on the link to the image
    browser.find_by_css('a.product-item h3')[i].click()
    
    # Once clicked - sample displays the full resolution image we want
    image_link = browser.links.find_by_text('Sample').first
    hemisphere["img_url"] = image_link["href"]
    
    # Scrape the title
    hemisphere["title"] = browser.find_by_css("h2.title").text
    hemisphere_image_urls.append(hemisphere)
    
    #navigate back to the beginning to get the next hemisphere image.
    browser.back()


    


# In[90]:


# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls


# In[91]:


# 5. Quit the browser
browser.quit()


# In[ ]:





# In[ ]:




