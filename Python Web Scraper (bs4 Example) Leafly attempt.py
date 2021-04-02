#https://learningactors.com/how-to-scrape-multiple-pages-of-a-website-using-a-python-web-scraper/

import requests
from requests import get
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import re
from time import sleep
from random import randint


#Custom HTTP Header added to request
#headers = {"Accept-Language": "en-US,en;q=0.5"}

# Empty lists to store the scraped data

strains = []
ratings = []
thc_percts = []
strain_types = []

pages = np.arange(1, 166, 1) # 165 Total Pages to look through

for page in pages: 

  page = requests.get("https://www.leafly.com/strains?page=" + str(page))

  soup = BeautifulSoup(page.text, 'html.parser')
  strain_div = soup.find_all('div', class_='relative flex flex-col justify-between h-full w-full elevation-low rounded bg-white')
  
  sleep(randint(2,6)) # Control Crawl Rate

  for container in strain_div:

        strain = container.find('span', itemprop = 'name').text
        #strain = strain.astype(str)
        strains.append(strain) # Strain column is type String
        
        rating = container.find('span', class_ = 'pr-xs').text if container.find('span', class_ = 'pr-xs') else '-'
        #rating = float(rating) # Convert to Float for decimal number
        #Removed above because some were NULL and need to clean after all have been scraped
        ratings.append(rating)

        thc_perct = container.find('div', class_='inline-block font-bold text-xs bg-deep-green-20 py-xs px-sm rounded').text if container.find('div', class_='inline-block font-bold text-xs bg-deep-green-20 py-xs px-sm rounded') else '-'

        thc_percts.append(thc_perct)


        strain_type = container.find('div', class_= 'inline-block font-bold text-xs bg-leafly-white py-xs px-sm rounded mr-xs').text if container.find('div', class_= 'inline-block font-bold text-xs bg-leafly-white py-xs px-sm rounded mr-xs') else '-'
        strain_types.append(strain_type)


weed = pd.DataFrame({
'strain': strains,
'rating': ratings,
'strain_type': strain_types,
'thc_perct': thc_percts
})

weed['strain'] = weed['strain'].astype(str)

weed['rating'] = pd.to_numeric(weed['rating'], errors= 'coerce')

weed['thc_perct'] = weed['thc_perct'].astype(str) # Convert column to string for cleaning
weed['thc_perct'] = weed['thc_perct'].str.extract('(\d+)', expand = False) # Remove Non-Numeric characters
weed['thc_perct'] = pd.to_numeric(weed['thc_perct'], errors= 'coerce') # Convert to Integer

# to see your dataframe
print(weed)

# to see the datatypes of your columns
print(weed.dtypes)


# to see where you're missing data and how much data is missing 
print(weed.isnull().sum())

# to move all your scraped data to a CSV file
weed.to_csv('leafly_cannabis_scraped_data.csv', index = False)
