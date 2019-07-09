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
# I put a sleep into the loop because I received a timeout error previously. Could be due to too many requests to the 
# website or having a temporary connection issue.
for i in range(len(weapLinks)):
    weapCrawl = requests.get('https://escapefromtarkov.gamepedia.com' + weapLinks[i])
    weapSrc = weapCrawl.content.decode('utf-8')
    weapSoup = bs(weapSrc, 'lxml')
    time.sleep(0.5)
    for link in weapSoup.find_all('a', accesskey = 'e'):
        fullLinks.append('https://escapefromtarkov.gamepedia.com' + link.get('href'))

# Output all edit page links
#fullLinks

######
# Weapons links End
######

######
# Start setup
######

#Initalize category list
colmns = ['itemtypeid','slotid','name','weight','gridsize','price','traderid','opres','rarity','repair','firemodes',
           'sightingrange','ergo','muzzlevelocity','effectivedistance','accuracy','recoilvert',
           'recoilhoriz','rpm','caliber','defaultammo','defaultmag']

######
# End setup
######

######
# Start dataframe creation
######

# Only using the first 64 links as the weapon type changes so there is a different number of columns needed
Links = fullLinks[0:63]

# Creates empty dataframe for the weapon stats
weaponDF = pd.DataFrame()

# Loops through the links parsing the webpage and storing the data as beautiful soup
for i in range(len(Links)):
    time.sleep(0.5)
    webpage = requests.get(Links[i])
    webpageSrc = webpage.content.decode('utf-8')
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
    
     # Removes the <br/> tag then duplicates itself so the veritcal and horizontal recoil can be split
    data[16] = re.sub(r'<br/>', ' ', data[16])
    data.insert(16, data[16])

    # Initialize an empty list
    weaponList = []
        
    #weaponDF[gunName] = weaponList   
    if len(weaponDF) > 0:
        # Store new gun in second dataframe    
        weaponDF2 = pd.DataFrame([data], columns = colmns)              
        
        # Append df2 to original df
        weaponDF = weaponDF.append(weaponDF2)      
    else:
        weaponDF = pd.DataFrame([data], columns = colmns)
   
######
# End dataframe creation
######

###############
# Start Dataframe cleanup
###############

# Removes weapons and the type of weapon up to the | symbol
weaponDF['itemtypeid'].replace(to_replace=r'\[.+?\|', value = '', regex = True, inplace = True)    

# Removes the trailing bracket symbols
weaponDF['itemtypeid'].replace(to_replace=r'\]\]', value = '', regex = True, inplace = True)  
weaponDF['caliber'].replace(to_replace=r'\]\]', value = '', regex = True, inplace = True)  
weaponDF['defaultammo'].replace(to_replace=r'\]\]', value = '', regex = True, inplace = True)  

# Removes the leading bracket symbols
weaponDF['caliber'].replace(to_replace=r'\[\[', value = '', regex = True, inplace = True)  
weaponDF['defaultammo'].replace(to_replace=r'\[\[', value = '', regex = True, inplace = True)  

# Removes the leading | symbol
weaponDF['firemodes'].replace(to_replace=r'\|', value = '', regex = True, inplace = True)  
weaponDF['sightingrange'].replace(to_replace=r'\|', value = '', regex = True, inplace = True)
weaponDF['ergo'].replace(to_replace=r'\|', value = '', regex = True, inplace = True)  

# Removes vertical from the start and horizontal from the end just leaves the numbers
weaponDF['recoilvert'].replace(to_replace=r'Vertical: ', value = '', regex = True, inplace = True)  
weaponDF['recoilvert'].replace(to_replace=r' Horizontal:....', value = '', regex = True, inplace = True)

# Removes vertical from the start and horizontal from the end just leaves the numbers
weaponDF['recoilhoriz'].replace(to_replace=r'Vertical:.*?H', value = '', regex = True, inplace = True)  
weaponDF['recoilhoriz'].replace(to_replace=r'orizontal: ', value = '', regex = True, inplace = True)

# Removes the <br/> tag from this element
weaponDF['firemodes'].replace(to_replace=r'<br/>', value = ', ', regex = True, inplace = True)

# Removes |caliber=9x19mm
weaponDF['caliber'].replace(to_replace=r'\|.*?=', value = '', regex = True, inplace = True)


######
# End Dataframe cleanup
###### 

#####
# Start item type and slot ID conversions
#####
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

#####
# End item type and slot ID conversions
#####

len("Single, 3-round Burst, Full Auto")

#######
# Start SQL
#######

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

#######
# End SQL
#######

# column     
#print(weaponDF.iloc[:,0])

# row     
#print(weaponDF.iloc[30,:])