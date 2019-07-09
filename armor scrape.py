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
#	18	slots
#	19	name

armorCols = ['itemtypeid','slotid','weight','gridsize','price','traderid','rarity', 'material', 'armor', 'armorcoverage',
             'armorsegments', 'durability', 'ricochetchance', 'penalties','blocksarmor', 'blocksearpiece', 'blockseyewear', 
             'blocksfacecover','slots','name']
# armor
#webpage = requests.get('https://escapefromtarkov.gamepedia.com/index.php?title=6B43_6A_Armor&action=edit')

# rig
# webpage = requests.get('https://escapefromtarkov.gamepedia.com/index.php?title=BlackRock_chest_rig&action=edit')

# armored rig
#webpage = requests.get('https://escapefromtarkov.gamepedia.com/index.php?title=ANA_Tactical_M2_armored_rig&action=edit')

# helmet
#webpage = requests.get('https://escapefromtarkov.gamepedia.com/index.php?title=6B47_Helmet&action=edit')

# backpack
#webpage = requests.get('https://escapefromtarkov.gamepedia.com/index.php?title=Scav_Backpack&action=edit')

# Decode the page
webpageSrc = webpage.content.decode('utf-8')

# conver the page to beautiful soup format
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
 
# Rig
if re.match('\[\[Chest rigs\|Chest rig\]\]', data[0]):
    data.insert(7, 0)
    data.insert(10, 0)
    data.insert(12, 0)
    data.insert(15, 0)
    data.insert(16, 0)
    data.insert(17, 0)

# Armored chest rig
if re.match(r'.*Armored chest rig.*', data[0]):   
    data.insert(10, 0)
    data.insert(12, 0)
    data.insert(15, 0)
    data.insert(16, 0)
    data.insert(17, 0)
    
# helmet
if re.match(r'\[\[Headwear\]\]', data[1]):
    data.insert(14, 0)
    
# armor
if re.match(r'.*Armor vest.*', data[0]):
    data.insert(12, 0)
    data.insert(14, 0)
    data.insert(15, 0)
    data.insert(16, 0)
    data.insert(17, 0)

# Backpack

data[0]

# Add weapon name as position 2
data.insert(19, itemName)

testDF = pd.DataFrame([data], columns = armorCols)

testDF

print(testDF.iloc[0,:])

len(testDF)

############
# old method
############

# Initialize an empty list
#testList = []

# Use a loop to move the data into the list where a data element is present in the numbers list
# Otherwise include a 0

#len(colmns)
#
#for i in range(len(data)):
#    if i in numbers:
#        testList.append(data[i])
#    else:
#        testList.append(0)
#     
##weaponDF[gunName] = weaponList   
#
#testDF = pd.DataFrame([testList], columns = colmns)
 

