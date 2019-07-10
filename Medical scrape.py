# -*- coding: utf-8 -*-
"""
Created on Tue Jul  9 21:36:18 2019

@author: Eric Born
"""
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import re

#	0	type
#	1	slot
#	2	weight
#	3	grid
#	4	price
#	5	trader
#	6	rarity
#	7	effect
#	8	use time
#	9	spawn chance
#	10	loot xp
#	11	exam xp

######
# Start setup
######

#Initalize category list                
medCols = ['itemtypeid','slotid','weight','gridsize','price','traderid','rarity', 'effect', 'usetime', 
           'spawnchance', 'lootxp', 'examxp','name']

# Pulls down the full weapons page
webpage = requests.get('https://escapefromtarkov.gamepedia.com/Medical')

# Decodes the page
medsSrc = webpage.content.decode('utf-8')

# convert the page to beautiful soup format
soup = bs(medsSrc, 'lxml')

medLinks = []

# Store links in a list
for i in soup.find_all("table",{"class":"wikitable sortable"}):
    for th in i.find_all('th'):
        for link in th.find_all('a'):
            #print(link.get('href'))
            medLinks.append(link.get('href'))

# Links are duplicated due to the icon and the text being indivdual links to each armor
# converting to a set and back to a list makes them unique
medLinks = list(set(medLinks))

# Initialize a list that will store the edit page URL
fullLinks = []

# Loops through each main weapon URL then finds the link to the edit source page and writes it to the fullLinks list
# I put a sleep into the loop because I received a timeout error previously. Could be due to too many requests to the 
# website or having a temporary connection issue.
for i in range(len(medLinks)):
    medCrawl = requests.get('https://escapefromtarkov.gamepedia.com' + medLinks[i])
    medSrc = medCrawl.content.decode('utf-8')
    medSoup = bs(medSrc, 'lxml')
    #time.sleep(1)
    for link in medSoup.find_all('a', accesskey = 'e'):
        fullLinks.append('https://escapefromtarkov.gamepedia.com' + link.get('href'))

######
# End setup
######
        
# Creates empty dataframe for the weapon stats
medsDF = pd.DataFrame()

links = fullLinks[0:5]


webpage = requests.get(fullLinks[1])
webpageSrc = webpage.content.decode('utf-8')
soup = bs(webpageSrc, 'lxml')

# Grab item name from the firstHeading
itemName = soup.find('h1', id='firstHeading').text

# Remove editing from the start of the guns name
itemName = re.sub('Editing ', '', itemName)

# converts textarea to a string
text = str(soup.textarea.contents[0])

# splits on '|type' and only keeps the last indexed item by using -1
text = text.split(r'|type', 1)[-1]

# splits on '|ammo' and only keeps the first indexed item by using 0
text = text.split('\n|mods', 1)[0]

# splits on '\n'
data = text.split('\n')

# Loop that removes characters relating to the categories of the data
for i in range(len(data)):
    #data[i] = re.sub(r'\|.*=', '', data[i])
    data[i] = re.sub(r'.*=', '', data[0])




# Loops through the links parsing the webpage and storing the data as beautiful soup
for i in range(len(fullLinks)):
    #time.sleep(1)
    webpage = requests.get(fullLinks[i])
    webpageSrc = webpage.content.decode('utf-8')
    soup = bs(webpageSrc, 'lxml')

    # Grab item name from the firstHeading
    itemName = soup.find('h1', id='firstHeading').text
    
    # Remove editing from the start of the guns name
    itemName = re.sub('Editing ', '', itemName)
    
    # converts textarea to a string
    text = str(soup.textarea.contents[0])
    
    # splits on '|type' and only keeps the last indexed item by using -1
    text = text.split(r'|type', 1)[-1]
    
    # splits on '|ammo' and only keeps the first indexed item by using 0
    text = text.split('\n|mods', 1)[0]
    
    # splits on '\n'
    data = text.split('\n')
    
    # Loop that removes characters relating to the categories of the data
    for i in range(len(data)):
        #data[i] = re.sub(r'\|.*=', '', data[i])
        data[i] = re.sub(r'.*=', '', data[i])
        
    # Add weapon name as position 20
    data.insert(9, itemName)

    # checks if the dataframe already has any items in it. If it does it appends, if not it creates
    if len(medsDF) > 0:
        # Store new gun in second dataframe    
        medsDF2 = pd.DataFrame([data], columns = medCols)              
        
        # Append df2 to original df
        medsDF = medsDF.append(medsDF2)      
    else:
        medsDF = pd.DataFrame([data], columns = medCols)