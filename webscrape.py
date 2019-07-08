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
    if row['itemtypeid'] == 'Assault rifle':
        return 1
    elif row['itemtypeid'] == 'Assault carbine':
        return 2
    elif row['itemtypeid'] == 'Light machine gun':
        return 3
    elif row['itemtypeid'] == 'Submachine gun':
        return 4
    elif row['itemtypeid'] == 'Shotgun':
        return 5
    elif row['itemtypeid'] == 'Designated marksman rifle':
        return 6
    elif row['itemtypeid'] == 'Sniper rifle':
        return 7
    elif row['itemtypeid'] == 'Pistol':
        return 8
    elif row['itemtypeid'] == 'Melee weapon':
        return 9
    elif row['itemtypeid'] == 'Fragmentation grenade':
        return 10
    elif row['itemtypeid'] == 'Smoke grenade':
        return 11
    elif row['itemtypeid'] == 'Stun grenade':
        return 12
    elif row['itemtypeid'] == 'Mask':
        return 13
    elif row['itemtypeid'] == 'Armor vest':
        return 14
    elif row['itemtypeid'] == 'Helmet':
        return 15
    elif row['itemtypeid'] == 'Armored chest rig':
        return 16
    elif row['itemtypeid'] == 'Chest rig':
        return 17
    elif row['itemtypeid'] == 'Night vision':
        return 18
    elif row['itemtypeid'] == 'Goggles':
        return 19
    elif row['itemtypeid'] == 'Backpack':
        return 20
    
# Apply the function across the type column on all rows
weaponDF['itemtypeid'] = weaponDF.apply(itemTypeId, axis=1)

def slotId(row):
    if row['slotid'] == "Primary":
        return 1
    elif row['slotid'] == "Secondary":
        return 2
    elif row['slotid'] == "Melee":
        return 3
    elif row['slotid'] == "Headwear":
        return 4
    elif row['slotid'] == "Earpiece":
        return 5
    elif row['slotid'] == "Face Cover":
        return 6
    elif row['slotid'] == "Body Armor":
        return 7
    elif row['slotid'] == "Armband":
        return 8
    elif row['slotid'] == "Eyewear":
        return 9
    elif row['slotid'] == "Chest Rig":
        return 10
    elif row['slotid'] == "Backpack":
        return 11

# Apply slotID across the DF
weaponDF['slotid'] = weaponDF.apply(slotId, axis=1)

# Create new column for DEFAULT across all rows. Allows the auto increment in the database to function properly
#weaponDF['Default'] = str('DEFAULT')

# Grab column names
#cols = weaponDF.columns.tolist()

# Move the last column to the first position
#cols = cols[-1:] + cols[:-1]

# rebuild the df from the new cols list
#weaponDF = weaponDF[cols]

# print column 0 all rows
print(weaponDF.iloc[0,:])

#weaponDF.to_csv(r'd:\test.csv')

#weaponDF.head

# create dictionary from df
#weaponDict = weaponDF.to_dict('split')

# Store data types for the dataframe
#dtypeCount =[weaponDF.iloc[:,i].apply(type).value_counts() for i in range(weaponDF.shape[1])]

# access the data types
#dtypeCount

type(weaponDF.iloc[0,1])

weaponDF.dtypes

# Chance price to object instead of int due to currency 
weaponDF = weaponDF.astype({'price': object, })

# Change columns to numeric instead of object
weaponDF['sightingrange'] = pd.to_numeric(weaponDF['sightingrange'])
weaponDF['ergo'] = pd.to_numeric(weaponDF['ergo'])
weaponDF['recoilvert'] = pd.to_numeric(weaponDF['recoilvert'])
weaponDF['recoilhoriz'] = pd.to_numeric(weaponDF['recoilhoriz'])
weaponDF['rpm'] = pd.to_numeric(weaponDF['rpm'])



###############################
# SQL
#############

from sqlalchemy import create_engine, MetaData, insert, Table, Column, String, Integer, Float, Boolean, VARCHAR, SmallInteger
import psycopg2
import io

meta = MetaData()

# Creates a connection string
engine = create_engine('postgresql+psycopg2://TomBrody:pass@localhost/tarkov')

# Creates a table using the column names and datatypes defined in the dataframe
weaponDF.head(0).to_sql('weaponproperties', engine, if_exists = 'replace', index = False)

# raw connection
conn = engine.raw_connection()

# Opens a cursor to write the data
cur = conn.cursor()

# prepares an in memory IO stream
output = io.StringIO()

# converts the dataframe contents to csv format and the IO steam as its destination
weaponDF.to_csv(output, sep='\t', header=False, index=False)

# sets the file offset position to 0
output.seek(0)

# retrieves the contents of the output stream
contents = output.getvalue()

# Copys from the stream to the weaponproperties table
cur.copy_from(output, 'weaponproperties', null="") # null values become ''

# Commits on the connection to the database
conn.commit()


# Automatically reflects the database table and stores the column types and details
# weaponProperties = Table('weaponproperties', meta, autoload = True, autoload_with = engine)

# Revises table/column details to drop the weaponId column which is auto generated by postgres
weaponProperties = Table('weaponproperties', meta,
                         Column('itemtypeid', SmallInteger(), nullable=False),
                         Column('slotid', SmallInteger(), nullable=False), 
                         Column('name', VARCHAR(length=50)), 
                         Column('weight', VARCHAR(length=10)), 
                         Column('gridsize', VARCHAR(length=10)), 
                         Column('price', VARCHAR(length=5)), 
                         Column('traderid', SmallInteger()), 
                         Column('opres', SmallInteger), 
                         Column('rarity', SmallInteger), 
                         Column('repair', SmallInteger), 
                         Column('firemodes', VARCHAR(length=50)), 
                         Column('sightingrange', SmallInteger()), 
                         Column('ergo', SmallInteger()),
                         Column('muzzlevelocity', VARCHAR(length=10)), 
                         Column('effectivedistance', VARCHAR(length=6)), 
                         Column('accuracy', SmallInteger()), 
                         Column('recoilvert', SmallInteger()), 
                         Column('recoilhoriz', SmallInteger()), 
                         Column('rpm', SmallInteger()), 
                         Column('caliber', VARCHAR(length=30)), 
                         Column('defaultammo', VARCHAR(length=50)), 
                         Column('defaultmag', VARCHAR(length=50)), schema=None)

#res = engine.execute('SELECT * FROM weaponProperties;').fetchall()

# Selects all tables in the db
#print(engine.table_names())

# Maps out the insert statement
ins = weaponProperties.insert()

str(ins)

weaponDF.to_sql(weaponProperties, con = engine, if_exists = 'append', index = False)

#print(weaponDF.iloc[1,:])


#result = table.update().returning()

#stmt = insert(weaponProperties('weaponProperties'))


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