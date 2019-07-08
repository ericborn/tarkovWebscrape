# -*- coding: utf-8 -*-
"""
Created on Tue Jul  2 17:13:13 2019

@author: Eric Born

data extracted for the category and index positions
=============================================================================
#0 type
#1 slot
#2 weight
#3 grid size
#4 price
#5 trader
#6 op res
#7 rarity
#8 repair
#9 fire modes
#10 sight range
#11 ergo
#12 muzzle velo
#13 Effective distance
#14 accuracy
#15 recoil
#16 rpm
#17 caliber
#18 default ammo
#19 default mag
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
numbers = [0, 1, 2, 3, 9, 10, 11, 12, 13, 15, 16, 17, 18]

#Initalize category list
category = {'Category':['Type','Slot','Weight','Grid size','Price','Trader','Op Res','Rarity','Repair','Fire Modes',
                        'Sighting range','Ergonomics','Muzzle velocity','Effective distance','Accuracy','Vertical Recoil',
                        'Horizontal Recoil','Rate of fire (RPM)','Caliber','Default ammo','Default mag']}

# Create empty list to store the weapon data
weaponList = []

# Convert the categories into a dataframe 
weaponDF = pd.DataFrame(category)

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

# Removes weapons and the type of weapon up to the | symbol
data[0] = re.sub(r'\[.+?\|', '', data[0])
   
# Removes the trailing bracket symbols
data[0] = re.sub(r'\]\]', '', data[0])
data[17] = re.sub(r'\]\]', '', data[17])
data[18] = re.sub(r'\]\]', '', data[18])

# Removes the leading bracket symbols
data[17] = re.sub(r'\[\[', '', data[17])
data[18] = re.sub(r'\[\[', '', data[18])

# Removes the leading | symbol
data[10] = re.sub(r'\|', '', data[10])
data[11] = re.sub(r'\|', '', data[11])

# Removes the <br/> tag then duplicates itself so the veritcal and horizontal recoil can be split
data[15] = re.sub(r'<br/>', ' ', data[15])
data.insert(15, data[15])

# Removes vertical from the start and horizontal from the end just leaving the numbers
data[15] = re.sub(r'Vertical: ', '', data[15])
data[15] = re.sub(r' Horizontal:....', '', data[15])

# Removes vertical from the start and horizontal from the end just leaving the numbers
data[16] = re.sub(r'Vertical:.*?H', '', data[16])
data[16] = re.sub(r'orizontal: ', '', data[16])

# Removes the <br/> tag from this element
data[9] = re.sub(r'<br/>', ', ', data[9])

# Removes the | symbol
data[9] = re.sub(r'\|', '', data[9])

# Initialize an empty list
weaponList = []

# Use a loop to move the data into the list where a data element is present in the numbers list
# Otherwise include a 0
for i in range(len(data)):
    if i in numbers:
        weaponList.append(data[i])
    else:
        weaponList.append(0)
     
weaponDF[gunName] = weaponList                     

#weaponDF
 
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
  
# Removes weapons and the type of weapon up to the | symbol
data[0] = re.sub(r'\[.+?\|', '', data[0])
   
# Removes the trailing bracket symbols
data[0] = re.sub(r'\]\]', '', data[0])
data[17] = re.sub(r'\]\]', '', data[17])
data[18] = re.sub(r'\]\]', '', data[18])

# Removes the leading bracket symbols
data[17] = re.sub(r'\[\[', '', data[17])
data[18] = re.sub(r'\[\[', '', data[18])

# Removes the leading | symbol
data[10] = re.sub(r'\|', '', data[10])
data[11] = re.sub(r'\|', '', data[11])

# Removes the <br/> tag then duplicates itself so the veritcal and horizontal recoil can be split
data[15] = re.sub(r'<br/>', ' ', data[15])
data.insert(15, data[15])

# Removes vertical from the start and horizontal from the end just leaving the numbers
data[15] = re.sub(r'Vertical: ', '', data[15])
data[15] = re.sub(r' Horizontal:....', '', data[15])

# Removes vertical from the start and horizontal from the end just leaving the numbers
data[16] = re.sub(r'Vertical:....', '', data[16])
data[16] = re.sub(r' Horizontal: ', '', data[16])

# Removes the <br/> tag from this element
data[9] = re.sub(r'<br/>', ', ', data[9])

# Removes the | symbol
data[9] = re.sub(r'\|', '', data[9])

# Initialize an empty list
weaponList = []

# Use a loop to move the data into the list where a data element is present in the numbers list
# Otherwise include a 0
for i in range(len(data)):
    if i in numbers:
        weaponList.append(data[i])
    else:
        weaponList.append(0)
     
weaponDF[gunName] = weaponList                     

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
    
# Removes weapons and the type of weapon up to the | symbol
data[0] = re.sub(r'\[.+?\|', '', data[0])
   
# Removes the trailing bracket symbols
data[0] = re.sub(r'\]\]', '', data[0])
data[17] = re.sub(r'\]\]', '', data[17])
data[18] = re.sub(r'\]\]', '', data[18])

# Removes the leading bracket symbols
data[17] = re.sub(r'\[\[', '', data[17])
data[18] = re.sub(r'\[\[', '', data[18])

# Removes the leading | symbol
data[10] = re.sub(r'\|', '', data[10])
data[11] = re.sub(r'\|', '', data[11])

# Removes the <br/> tag then duplicates itself so the veritcal and horizontal recoil can be split
data[15] = re.sub(r'<br/>', ' ', data[15])
data.insert(15, data[15])

# Removes vertical from the start and horizontal from the end just leaving the numbers
data[15] = re.sub(r'Vertical: ', '', data[15])
data[15] = re.sub(r' Horizontal:....', '', data[15])

# Removes vertical from the start and horizontal from the end just leaving the numbers
data[16] = re.sub(r'Vertical:....', '', data[16])
data[16] = re.sub(r' Horizontal: ', '', data[16])

# Removes the <br/> tag from this element
data[9] = re.sub(r'<br/>', ', ', data[9])

# Removes the | symbol
data[9] = re.sub(r'\|', '', data[9])

# Initialize an empty list
weaponList = []

# Use a loop to move the data into the list where a data element is present in the numbers list
# Otherwise include a 0
for i in range(len(data)):
    if i in numbers:
        weaponList.append(data[i]) 
    else:
        weaponList.append(0)
     
weaponDF[gunName] = weaponList                     

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
    
# Removes weapons and the type of weapon up to the | symbol
data[0] = re.sub(r'\[.+?\|', '', data[0])
   
# Removes the trailing bracket symbols
data[0] = re.sub(r'\]\]', '', data[0])
data[17] = re.sub(r'\]\]', '', data[17])
data[18] = re.sub(r'\]\]', '', data[18])

# Removes the leading bracket symbols
data[17] = re.sub(r'\[\[', '', data[17])
data[18] = re.sub(r'\[\[', '', data[18])

# Removes the leading | symbol
data[10] = re.sub(r'\|', '', data[10])
data[11] = re.sub(r'\|', '', data[11])

# Removes the <br/> tag then duplicates itself so the veritcal and horizontal recoil can be split
data[15] = re.sub(r'<br/>', ' ', data[15])
data.insert(15, data[15])

# Removes vertical from the start and horizontal from the end just leaving the numbers
data[15] = re.sub(r'Vertical: ', '', data[15])
data[15] = re.sub(r' Horizontal:....', '', data[15])

# Removes vertical from the start and horizontal from the end just leaving the numbers
data[16] = re.sub(r'Vertical:....', '', data[16])
data[16] = re.sub(r' Horizontal: ', '', data[16])

# Removes the <br/> tag from this element
data[9] = re.sub(r'<br/>', ', ', data[9])

# Removes the | symbol
data[9] = re.sub(r'\|', '', data[9])

# Initialize an empty list
weaponList = []

# Use a loop to move the data into the list where a data element is present in the numbers list
# Otherwise include a 0
for i in range(len(data)):
    if i in numbers:
        weaponList.append(data[i])
    else:
        weaponList.append(0)
     
weaponDF[gunName] = weaponList                     

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
    
# Removes weapons and the type of weapon up to the | symbol
data[0] = re.sub(r'\[.+?\|', '', data[0])
   
# Removes the trailing bracket symbols
data[0] = re.sub(r'\]\]', '', data[0])
data[17] = re.sub(r'\]\]', '', data[17])
data[18] = re.sub(r'\]\]', '', data[18])

# Removes the leading bracket symbols
data[17] = re.sub(r'\[\[', '', data[17])
data[18] = re.sub(r'\[\[', '', data[18])

# Removes the leading | symbol
data[10] = re.sub(r'\|', '', data[10])
data[11] = re.sub(r'\|', '', data[11])

# Removes the <br/> tag then duplicates itself so the veritcal and horizontal recoil can be split
data[15] = re.sub(r'<br/>', ' ', data[15])
data.insert(15, data[15])

# Removes vertical from the start and horizontal from the end just leaving the numbers
data[15] = re.sub(r'Vertical: ', '', data[15])
data[15] = re.sub(r' Horizontal:....', '', data[15])

# Removes vertical from the start and horizontal from the end just leaving the numbers
data[16] = re.sub(r'Vertical:.*?H', '', data[16])
data[16] = re.sub(r'orizontal: ', '', data[16])

# Removes the <br/> tag from this element
data[9] = re.sub(r'<br/>', ', ', data[9])

# Removes the | symbol
data[9] = re.sub(r'\|', '', data[9])

# Initialize an empty list
weaponList = []

# Use a loop to move the data into the list where a data element is present in the numbers list
# Otherwise include a 0
for i in range(len(data)):
    if i in numbers:
        weaponList.append(data[i])
    else:
        weaponList.append(0)
     
weaponDF[gunName] = weaponList                     

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
    
# Removes weapons and the type of weapon up to the | symbol
data[0] = re.sub(r'\[.+?\|', '', data[0])
   
# Removes weapons and the type of weapon up to the | symbol
data[0] = re.sub(r'\[.+?\|', '', data[0])
   
# Removes the trailing bracket symbols
data[0] = re.sub(r'\]\]', '', data[0])
data[17] = re.sub(r'\]\]', '', data[17])
data[18] = re.sub(r'\]\]', '', data[18])

# Removes the leading bracket symbols
data[17] = re.sub(r'\[\[', '', data[17])
data[18] = re.sub(r'\[\[', '', data[18])

# Removes the leading | symbol
data[10] = re.sub(r'\|', '', data[10])
data[11] = re.sub(r'\|', '', data[11])

# Removes the <br/> tag then duplicates itself so the veritcal and horizontal recoil can be split
data[15] = re.sub(r'<br/>', ' ', data[15])
data.insert(15, data[15])

# Removes vertical from the start and horizontal from the end just leaving the numbers
data[15] = re.sub(r'Vertical: ', '', data[15])
data[15] = re.sub(r' Horizontal:....', '', data[15])

# Removes vertical from the start and horizontal from the end just leaving the numbers
data[16] = re.sub(r'Vertical:....', '', data[16])
data[16] = re.sub(r' Horizontal: ', '', data[16])

# Removes the <br/> tag from this element
data[9] = re.sub(r'<br/>', ', ', data[9])

# Removes the | symbol
data[9] = re.sub(r'\|', '', data[9])

# Initialize an empty list
weaponList = []

# Use a loop to move the data into the list where a data element is present in the numbers list
# Otherwise include a 0
for i in range(len(data)):
    if i in numbers:
        weaponList.append(data[i])
    else:
        weaponList.append(0)
     
weaponDF[gunName] = weaponList                     

print(weaponDF.iloc[15,:])

#####
# End gun 6
#####

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