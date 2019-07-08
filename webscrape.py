# -*- coding: utf-8 -*-
"""
Created on Tue Jul  2 17:13:13 2019

@author: Eric Born

data extracted for the category and index positions
=============================================================================
#0 type
#1 slot
#2 name
#3 weight
#4 grid size
#5 price
#6 trader
#7 op res
#8 rarity
#9 repair
#10 fire modes
#11 sight range
#12 ergo
#13 muzzle velo
#14 Effective distance
#15 accuracy
#16 recoil
#17 rpm
#18 caliber
#19 default ammo
#20 default mag
=============================================================================

Create a mapping for item type and slot to an int for the slot and itemType tables

pull out recoil vertical and horizontal into individual items

mapping for tradersId to name
"""

import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import re

######
# Start setup
######
# Creates a number set that corresponds to the categorys we're actully pulling data in from
numbers = [0, 1, 2, 3, 4, 10, 11, 12, 13, 14, 16, 17, 18, 19, 20]

#Initalize category list
colmns = ['itemTypeId','slotId','name','weight','gridSize','price','traderId','opRes','rarity','repair','fireModes',
           'sightingRange','ergonomics','muzzleVelocity','effectiveDistance','accuracy','recoilVert',
           'recoilHoriz','rpm','caliber','defaultAmmo','defaultMag']

# Convert the categories into a dataframe 
#weaponDF = pd.DataFrame(columns)

######
# End setup
######

#####
# Start gun 1
#####

# Pull down weapon page
webpage = requests.get('https://escapefromtarkov.gamepedia.com/index.php?title=DS_Arms_SA-58_7.62x51&action=edit')

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

#####
# Start gun 2
#####

# Pull down weapon page
webpage = requests.get("https://escapefromtarkov.gamepedia.com/index.php?title=AK-74N_5.45x39_assault_rifle&action=edit")

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

# Checks to see if the category op res is missing by looking at the content of the 7th and 8th index for fire mode |Single
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

# Store new gun in second dataframe    
weaponDF2 = pd.DataFrame([weaponList], columns = colmns)              

# Append df2 to original df
weaponDF = weaponDF.append(weaponDF2)

#weaponDF.iloc[0,:]

#####
# Start gun 2
#####

#####
# Start gun 3
#####

# Pull down weapon page
webpage = requests.get('https://escapefromtarkov.gamepedia.com/index.php?title=DVL-10_Saboteur_sniper_rifle&action=edit')

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
     
# Store new gun in second dataframe    
weaponDF2 = pd.DataFrame([weaponList], columns = colmns)              

# Append df2 to original df
weaponDF = weaponDF.append(weaponDF2)

#####
# End gun 3
#####   

#####
# Start gun 4
#####

# Pull down weapon page
webpage = requests.get("https://escapefromtarkov.gamepedia.com/index.php?title=Colt_M4A1_5.56x45_Assault_Rifle&action=edit")

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
     
# Store new gun in second dataframe    
weaponDF2 = pd.DataFrame([weaponList], columns = colmns)              

# Append df2 to original df
weaponDF = weaponDF.append(weaponDF2)

#print(weaponDF.iloc[1,:])

#####
# End gun 4
#####  

#####
# Start gun 5
#####

# Pull down weapon page
webpage = requests.get("https://escapefromtarkov.gamepedia.com/index.php?title=HK_MP5_9x19_submachinegun_(Navy_3_Round_Burst)&action=edit")

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
     
# Store new gun in second dataframe    
weaponDF2 = pd.DataFrame([weaponList], columns = colmns)              

# Append df2 to original df
weaponDF = weaponDF.append(weaponDF2)

#print(weaponDF.iloc[1,:])

#####
# End gun 5
#####

#####
# Start gun 6
#####

# Pull down weapon page
webpage = requests.get("https://escapefromtarkov.gamepedia.com/index.php?title=Remington_Model_870_12ga_shotgun&action=edit")

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
     
# Store new gun in second dataframe    
weaponDF2 = pd.DataFrame([weaponList], columns = colmns)              

# Append df2 to original df
weaponDF = weaponDF.append(weaponDF2)

#####
# End gun 6
#####

###################################

# Creates a function that converts the item type to the database number
def itemTypeId(row):
    if row['itemTypeId'] == 'Assault rifle':
        return 1
    elif row['itemTypeId'] == 'Assault carbine':
        return 2
    elif row['itemTypeId'] == 'Light machine gun':
        return 3
    elif row['itemTypeId'] == 'Submachine gun':
        return 4
    elif row['itemTypeId'] == 'Shotgun':
        return 5
    elif row['itemTypeId'] == 'Designated marksman rifle':
        return 6
    elif row['itemTypeId'] == 'Sniper rifle':
        return 7
    elif row['itemTypeId'] == 'Pistol':
        return 8
    elif row['itemTypeId'] == 'Melee weapon':
        return 9
    elif row['itemTypeId'] == 'Fragmentation grenade':
        return 10
    elif row['itemTypeId'] == 'Smoke grenade':
        return 11
    elif row['itemTypeId'] == 'Stun grenade':
        return 12
    elif row['itemTypeId'] == 'Mask':
        return 13
    elif row['itemTypeId'] == 'Armor vest':
        return 14
    elif row['itemTypeId'] == 'Helmet':
        return 15
    elif row['itemTypeId'] == 'Armored chest rig':
        return 16
    elif row['itemTypeId'] == 'Chest rig':
        return 17
    elif row['itemTypeId'] == 'Night vision':
        return 18
    elif row['itemTypeId'] == 'Goggles':
        return 19
    elif row['itemTypeId'] == 'Backpack':
        return 20
    
# Apply the function across the type column on all rows
weaponDF['itemTypeId'] = weaponDF.apply(itemTypeId, axis=1)

def slotId(row):
    if row['slotId'] == "Primary":
        return 1
    elif row['slotId'] == "Secondary":
        return 2
    elif row['slotId'] == "Melee":
        return 3
    elif row['slotId'] == "Headwear":
        return 4
    elif row['slotId'] == "Earpiece":
        return 5
    elif row['slotId'] == "Face Cover":
        return 6
    elif row['slotId'] == "Body Armor":
        return 7
    elif row['slotId'] == "Armband":
        return 8
    elif row['slotId'] == "Eyewear":
        return 9
    elif row['slotId'] == "Chest Rig":
        return 10
    elif row['slotId'] == "Backpack":
        return 11

# Apply slotID across the DF
weaponDF['slotId'] = weaponDF.apply(slotId, axis=1)

# Create new column for DEFAULT across all rows. Allows the auto increment in the database to function properly
#weaponDF['Default'] = str('DEFAULT')

# Grab column names
#cols = weaponDF.columns.tolist()

# Move the last column to the first position
#cols = cols[-1:] + cols[:-1]

# rebuild the df from the new cols list
#weaponDF = weaponDF[cols]

# print column 0 all rows
print(weaponDF.iloc[1,:])

# create dictionary from df
#weaponDict = weaponDF.to_dict('split')

# Store data types for the dataframe
#dtypeCount =[weaponDF.iloc[:,i].apply(type).value_counts() for i in range(weaponDF.shape[1])]

# access the data types
#dtypeCount

###############################
# All primary weapons
#rifleLinks = requests.get('https://escapefromtarkov.gamepedia.com/Weapons#Assault_rifles')
#srcRifles = rifleLinks.content.decode('utf-8')
#rifleSoup = bs(srcRifles, 'lxml')


# Need to create while loop or if statement to using starting link and stopping link
#Start
#https://escapefromtarkov.gamepedia.com/ADAR_2-15
#https://escapefromtarkov.gamepedia.com/TT_pistol_(gold)
#end

#for link in rifleSoup.find_all('a'):
#    print(link.get('href'))

# All primary weapons
###############################