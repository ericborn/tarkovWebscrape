# -*- coding: utf-8 -*-
"""
Created on Mon Jul  8 13:42:19 2019

@author: Eric Born
"""
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import re
import time

###############################
# Weapons links start
###############################

# Pulls down the full weapons page
weaponPage = requests.get('https://escapefromtarkov.gamepedia.com/Weapons#Assault_rifles')

# Decodes the page
weaponSrc = weaponPage.content.decode('utf-8')

# convert the page to beautiful soup format
soup = bs(weaponSrc, 'lxml')

# Creates an empty list to store all weapon main view page links
weapLinks = []

# Store links in a list
for link in soup.find_all('a', class_ = "mw-redirect"):
    #print(link.get('href'))
    weapLinks.append(link.get('href'))

# Base URL
# https://escapefromtarkov.gamepedia.com

# Weapon main view page
# https://escapefromtarkov.gamepedia.com/Yarygin_MP-443_Grach_9x19_pistol

# Weapon edit page, replace XXX with weapon name
# https://escapefromtarkov.gamepedia.com/index.php?title=Yarygin_MP-443_Grach_9x19_pistol&action=edit

# Initialize a list that will store the edit page URL
fullLinks = []

# Loops through each main weapon URL then finds the link to the edit source page and writes it to the fullLinks list
# Put a sleep into the loop because I received a timeout error previously. Could be due to too many requests to the 
# website or having a connection issue.
for i in range(len(weapLinks)):
    weapCrawl = requests.get('https://escapefromtarkov.gamepedia.com' + weapLinks[i])
    weapSrc = weapCrawl.content.decode('utf-8')
    weapSoup = bs(weapSrc, 'lxml')
    time.sleep(1)
    for link in weapSoup.find_all('a', accesskey = 'e'):
        fullLinks.append('https://escapefromtarkov.gamepedia.com' + link.get('href'))

fullLinks 
    
  
# Removes / symbol before each link
#for link in range(len(WeapLinks)):
#   WeapLinks[link] = re.sub(r'/', '', WeapLinks[link])

#!!!!!!!!!!!! BREAKS LINKS !!!!!!!!!!!!!
# Replaces all % symbols with a quote "
#for link in range(len(WeapLinks)):
#    WeapLinks[link] = re.sub(r'%', '"', WeapLinks[link])    
    
    
    
    
    
    
testcrawl = requests.get('https://escapefromtarkov.gamepedia.com' + WeapLinks[125])
testSrc = testcrawl.content.decode('utf-8')
testSoup = bs(testSrc, 'lxml')

for link in testSoup.find_all('a', accesskey = 'e'):
    print('https://escapefromtarkov.gamepedia.com' + link.get('href'))






testLinks = 

WeapLinks[0] = re.sub(r'/', '', WeapLinks[0])


    
for link in soup.find_all('a', class_ = "mw-redirect"):
    #print(link.get('href'))
    WeapLinks.append('https://escapefromtarkov.gamepedia.com/index.php?title=' + link.get('href') + '&action=edit')    
    
    
    
WeapLinks[125]

###############################
# Weapons links End
###############################

######
# Start setup
######
# Creates a number set that corresponds to the categorys we're actully pulling data in from
numbers = [0, 1, 2, 3, 4, 10, 11, 12, 13, 14, 16, 17, 18, 19, 20]

#Initalize category list
colmns = ['itemtypeid','slotid','name','weight','gridsize','price','traderid','opres','rarity','repair','firemodes',
           'sightingrange','ergo','muzzlevelocity','effectivedistance','accuracy','recoilvert',
           'recoilhoriz','rpm','caliber','defaultammo','defaultmag']

# Convert the categories into a dataframe 
#weaponDF = pd.DataFrame(columns)

######
# End setup
######

#####
# Start gun 1
#####

# Pull down weapon page
webpage = requests.get(WeapLinks[125])

# Decode the page
webpageSrc = webpage.content.decode('utf-8')

# conver the page to beautiful soup format
soup = bs(webpageSrc, 'lxml')

# Grab gun name from the firstHeading
gunName = soup.find('h1', id='firstHeading').text

# Remove editing from the start of the guns name
gunName = re.sub('Editing ', '', gunName)

# converts textarea to a string
text = str(soup.textarea.contents[0])

# splits on '|type' and only keeps the last indexed item by using -1
text = text.split('|type', 1)[-1]

# splits on '|ammo' and only keeps the first indexed item by using 0
text = text.split('|ammo', 1)[0]

# splits on '\n'
data = text.split('\n')

# Loop that removes characters relating to the categories of the data
for i in range(len(data)):
    data[i] = re.sub(r'^|..........\s+[=$]', '', data[i])
    
# Checks to see if the category op res is missing by looking at the content of the 8th index for fire mode |Single
# If true it inserts an extra 0 into the list in the 6th index where op res should've been
if re.match(r'\|Single', data[7]):
    data.insert(6, 0)

if re.match(r'\|Single', data[8]):
    data.insert(6, 0)
    
# Add weapon name as position 2
data.insert(2, gunName)

# Removes weapons and the type of weapon up to the | symbol
data[0] = re.sub(r'\[.+?\|', '', data[0])
   
# Removes the trailing bracket symbols
data[0] = re.sub(r'\]\]', '', data[0])
data[18] = re.sub(r'\]\]', '', data[18])
data[19] = re.sub(r'\]\]', '', data[19])

# Removes the leading bracket symbols
data[18] = re.sub(r'\[\[', '', data[18])
data[19] = re.sub(r'\[\[', '', data[19])

# Removes the leading | symbol
data[11] = re.sub(r'\|', '', data[11])
data[12] = re.sub(r'\|', '', data[12])

# Removes the <br/> tag then duplicates itself so the veritcal and horizontal recoil can be split
data[16] = re.sub(r'<br/>', ' ', data[16])
data.insert(16, data[16])

# Removes vertical from the start and horizontal from the end just leaving the numbers
data[16] = re.sub(r'Vertical: ', '', data[16])
data[16] = re.sub(r' Horizontal:....', '', data[16])

# Removes vertical from the start and horizontal from the end just leaving the numbers
data[17] = re.sub(r'Vertical:.*?H', '', data[17])
data[17] = re.sub(r'orizontal: ', '', data[17])

# Removes the <br/> tag from this element
data[10] = re.sub(r'<br/>', ', ', data[10])

# Removes the | symbol
data[10] = re.sub(r'\|', '', data[10])

# Initialize an empty list
weaponList = []

# Use a loop to move the data into the list where a data element is present in the numbers list
# Otherwise include a 0
for i in range(len(data)):
    if i in numbers:
        weaponList.append(data[i])
    else:
        weaponList.append(0)
     
#weaponDF[gunName] = weaponList   

weaponDF = pd.DataFrame([weaponList], columns = colmns)
 
#####
# End gun 1
#####   



########
# Sample Code
########

#for link in rifleSoup.find_all('a'):
#    print(link.get('href'))
#
#for link in rifleSoup.find_all('a'):
#    links.append(link.get('href'))
