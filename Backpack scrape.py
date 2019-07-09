# -*- coding: utf-8 -*-
"""
Created on Mon Jul  8 22:08:44 2019

@author: Eric Born
"""
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import re

#	0	itemid
#	1	slot
#	2	weight
#	3	grid
#	4	price
#	5	trader
#	6	rarity
#	7	material
#	8	armor
#	9	armor coverage
#	10	armor segments
#	11	durability
#	12	ricochet chance
#	13	penalties
#	14	blocks armor
#	15	blocks ear
#	16	blocks eye
#	17	blocks face
#	18	blocks headwear
#	19	slots
#	20	name

armorCols = ['itemtypeid','slotid','weight','gridsize','price','traderid','rarity', 'material', 'armor', 'armorcoverage',
             'armorsegments', 'durability', 'ricochetchance', 'penalties','blocksarmor', 'blocksearpiece', 'blockseyewear', 
             'blocksfacecover','blocksheadwear','slots','name']
# body armor
#webpage = requests.get('https://escapefromtarkov.gamepedia.com/Armor_vests')

# rigs
# webpage = requests.get('https://escapefromtarkov.gamepedia.com/Chest_rigs')

# helmet
# webpage = requests.get('https://escapefromtarkov.gamepedia.com/Helmet')

# backpack
webpage = requests.get('https://escapefromtarkov.gamepedia.com/Backpacks')

# Earpieces
# webpage = requests.get('https://escapefromtarkov.gamepedia.com/Earpieces')

# Headwear
# webpage = requests.get('https://escapefromtarkov.gamepedia.com/Headwear')

# Decode the page
webpageSrc = webpage.content.decode('utf-8')

# conver the page to beautiful soup format
soup = bs(webpageSrc, 'lxml')

# Creates an empty list to store all weapon main view page links
backpackLinks = []

# Store links in a list
for i in soup.find_all("table",{"class":"wikitable sortable"}):
    for link in i.find_all('a'):
        #print(link.get('href'))
        backpackLinks.append(link.get('href'))

# Links are duplicated due to the icon and the text being indivdual links to each armor
# converting to a set and back to a list makes them unique
backpackLinks = list(set(backpackLinks))

# Initialize a list that will store the edit page URL
fullLinks = []

# Loops through each main weapon URL then finds the link to the edit source page and writes it to the fullLinks list
# I put a sleep into the loop because I received a timeout error previously. Could be due to too many requests to the 
# website or having a temporary connection issue.
for i in range(len(backpackLinks)):
    backpackCrawl = requests.get('https://escapefromtarkov.gamepedia.com' + backpackLinks[i])
    backpackSrc = backpackCrawl.content.decode('utf-8')
    backpackSoup = bs(backpackSrc, 'lxml')
    #time.sleep(1)
    for link in backpackSoup.find_all('a', accesskey = 'e'):
        fullLinks.append('https://escapefromtarkov.gamepedia.com' + link.get('href'))


# Creates empty dataframe for the weapon stats
backpackDF = pd.DataFrame()

links = fullLinks[10:15]

# Loops through the links parsing the webpage and storing the data as beautiful soup
for i in range(len(links)):
    #time.sleep(1)
    webpage = requests.get(links[i])
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
    text = text.split('\n|spawn', 1)[0]
    
    # splits on '\n'
    data = text.split('\n')
    
    # Loop that removes characters relating to the categories of the data
    for i in range(len(data)):
        #data[i] = re.sub(r'\|.*=', '', data[i])
        data[i] = re.sub(r'.*=', '', data[i])
    
    ########### Tactical Rig 
    # Rig
    if re.match('.*?\[\[Chest rigs\|Chest rig\]\]', data[0]):
        data.insert(7, 0)
        data.insert(10, 0)
        data.insert(12, 0)
        data.insert(15, 0)
        data.insert(16, 0)
        data.insert(17, 0)
        data.insert(18, 0)
    
    # Armored chest rig
    if re.match(r'.*Armored chest rig.*', data[0]):   
        data.insert(10, 0)
        data.insert(12, 0)
        data.insert(15, 0)
        data.insert(16, 0)
        data.insert(17, 0)
        data.insert(18, 0)
    
    ########### Body    
    # armor
    if re.match(r'.*Armor vest.*', data[0]):
        data.insert(10, 0)
        data.insert(12, 0)
        data.insert(14, 0)
        data.insert(15, 0)
        data.insert(16, 0)
        data.insert(17, 0)
        data.insert(18, 0)
    
    ########### Backpack
    # Backpack
    if re.match(r'.*Backpack.*', data[1]):    
        data.insert(7, 0)
        data.insert(10, 0)
        data.insert(12, 0)
        data.insert(14, 0)
        data.insert(15, 0)
        data.insert(16, 0)
        data.insert(17, 0)
        data.insert(18, 0)
    
    ########### Headwear
    # helmet
    if re.match(r'.*Helmet.*', data[0]):
        data.insert(14, 0)
        data.insert(18, 0)
        
    # Headmount
    if re.match(r'.*Head Mount.*', data[0]):  
        data.insert(10, 0)
        data.insert(12, 0)
        data.insert(14, 0)
        data.insert(18, 0)
          
    # hat/cap/bandana
    if any(re.match(regex_str, data[0]) for regex_str in [r'.*Hat.*', r'.*Cap.*', r'.*Bandana.*', r'.*Mask.*']):  
        data.insert(10, 0)
        data.insert(12, 0)
        data.insert(14, 0)
        data.insert(15, 0)
        data.insert(16, 0)
        data.insert(17, 0)
        data.insert(18, 0)
    
    ########### Earpiece
    # headset
    if re.match(r'.*Headset.*', data[0]):   
        data.insert(7, 0)
        data.insert(10, 0)
        data.insert(12, 0)
        data.insert(14, 0)
        data.insert(15, 0)
    
    #data[0]
    
    # Add weapon name as position 20
    data.insert(20, itemName)

    # checks if the dataframe already has any items in it. If it does it appends, if not it creates
    if len(backpackDF) > 0:
        # Store new gun in second dataframe    
        backpackDF2 = pd.DataFrame([data], columns = armorCols)              
        
        # Append df2 to original df
        backpackDF = backpackDF.append(backpackDF2)      
    else:
        backpackDF = pd.DataFrame([data], columns = armorCols)


print(backpackDF.iloc[0,:])

print(backpackDF.iloc[:,20])

len(backpackDF)