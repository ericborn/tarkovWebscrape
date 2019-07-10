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

# Eyewear
webpage = requests.get('https://escapefromtarkov.gamepedia.com/Eyewear')

# Decode the page
webpageSrc = webpage.content.decode('utf-8')

# conver the page to beautiful soup format
soup = bs(webpageSrc, 'lxml')

# Creates an empty list to store all weapon main view page links
armorLinks = []

# Store links in a list
for i in soup.find_all("table",{"class":"wikitable sortable"}):
    for link in i.find_all('a'):
        #print(link.get('href'))
        armorLinks.append(link.get('href'))

# Links are duplicated due to the icon and the text being indivdual links to each armor
# converting to a set and back to a list makes them unique
armorLinks = list(set(armorLinks))

# Initialize a list that will store the edit page URL
fullLinks = []

# Loops through each main weapon URL then finds the link to the edit source page and writes it to the fullLinks list
# I put a sleep into the loop because I received a timeout error previously. Could be due to too many requests to the 
# website or having a temporary connection issue.
for i in range(len(armorLinks)):
    armorCrawl = requests.get('https://escapefromtarkov.gamepedia.com' + armorLinks[i])
    armorSrc = armorCrawl.content.decode('utf-8')
    armorSoup = bs(armorSrc, 'lxml')
    #time.sleep(1)
    for link in armorSoup.find_all('a', accesskey = 'e'):
        fullLinks.append('https://escapefromtarkov.gamepedia.com' + link.get('href'))


# Creates empty dataframe for the weapon stats
armorDF = pd.DataFrame()

#links = fullLinks[15:20]

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
    text = text.split('\n|spawn', 1)[0]
    
    # splits on '\n'
    data = text.split('\n')
    
    # Loop that removes characters relating to the categories of the data
    for i in range(len(data)):
        #data[i] = re.sub(r'\|.*=', '', data[i])
        data[i] = re.sub(r'.*=', '', data[i])
    
    ########### Eyewear
    # Eyewear
    if re.match(r'.*Eyewear.*', data[1]):   
        data.insert(7, 0)
        data.insert(10, 0)
        data.insert(12, 0)
        data.insert(14, 0)
        data.insert(15, 0)
        data.insert(16, 0)
        data.insert(17, 0)
        data.insert(18, 0)
    
    # Add weapon name as position 20
    data.insert(20, itemName)

    # checks if the dataframe already has any items in it. If it does it appends, if not it creates
    if len(armorDF) > 0:
        # Store new gun in second dataframe    
        armorDF2 = pd.DataFrame([data], columns = armorCols)              
        
        # Append df2 to original df
        armorDF = armorDF.append(armorDF2)      
    else:
        armorDF = pd.DataFrame([data], columns = armorCols)

# Removes weapons and the type of weapon up to the | symbol
armorDF['slotid'].replace(to_replace=r'\[\[', value = '', regex = True, inplace = True)
armorDF['traderid'].replace(to_replace=r'\[\[', value = '', regex = True, inplace = True)     

# Removes the trailing bracket symbols
armorDF['slotid'].replace(to_replace=r'\]\]', value = '', regex = True, inplace = True)  
armorDF['traderid'].replace(to_replace=r'\]\]', value = '', regex = True, inplace = True)  

armorDF['penalties'].replace(to_replace=r'<\/font>', value = '', regex = True, inplace = True)  
armorDF['penalties'].replace(to_replace=r'"green">', value = '', regex = True, inplace = True)  

armorDF['blocksearpiece'].replace(to_replace=r'<\/font>', value = '', regex = True, inplace = True)  
armorDF['blocksearpiece'].replace(to_replace=r'"green">', value = '', regex = True, inplace = True)  

armorDF['blockseyewear'].replace(to_replace=r'<\/font>', value = '', regex = True, inplace = True)  
armorDF['blockseyewear'].replace(to_replace=r'"green">', value = '', regex = True, inplace = True)  

armorDF['blockseyewear'].replace(to_replace=r'<\/font>', value = '', regex = True, inplace = True)  
armorDF['blockseyewear'].replace(to_replace=r'"green">', value = '', regex = True, inplace = True)  

armorDF['blocksfacecover'].replace(to_replace=r'<\/font>', value = '', regex = True, inplace = True)  
armorDF['blocksfacecover'].replace(to_replace=r'"green">', value = '', regex = True, inplace = True)  

armorDF['penalties'].replace(to_replace=r'"red">', value = '', regex = True, inplace = True)
armorDF['blocksearpiece'].replace(to_replace=r'"red">', value = '', regex = True, inplace = True)
armorDF['blockseyewear'].replace(to_replace=r'"red">', value = '', regex = True, inplace = True)
armorDF['blocksfacecover'].replace(to_replace=r'"red">', value = '', regex = True, inplace = True)

# Removes the <br/> tag from this element
armorDF['traderid'].replace(to_replace=r'<br/>', value = ', ', regex = True, inplace = True)
armorDF['price'].replace(to_replace=r'<br/>', value = ', ', regex = True, inplace = True)
armorDF['ricochetchance'].replace(to_replace=r'<br/>', value = ', ', regex = True, inplace = True)

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
armorDF['itemtypeid'] = armorDF.apply(itemTypeId, axis=1)

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
    elif row['slotid'] == "Face cover":
        return 6
    elif row['slotid'] == "Body armor":
        return 7
    elif row['slotid'] == "Armband":
        return 8
    elif row['slotid'] == "Eyewear":
        return 9
    elif row['slotid'] == "Chest rig":
        return 10
    elif row['slotid'] == "Backpack":
        return 11
    
# Apply slotID across the DF
armorDF['slotid'] = armorDF.apply(slotId, axis=1)

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
armorDF.head(0).to_sql('equipmentproperties', engine, if_exists = 'append', index = False)

# raw connection
conn = engine.raw_connection()

# Opens a cursor to write the data
cur = conn.cursor()

# prepares an in memory IO stream
output = io.StringIO()

# converts the dataframe contents to csv format and the IO steam as its destination
armorDF.to_csv(output, sep='\t', header=False, index=False)

# sets the file offset position to 0
output.seek(0)

# retrieves the contents of the output stream
contents = output.getvalue()

# Copys from the stream to the weaponproperties table
cur.copy_from(output, 'equipmentproperties', null="") # null values become ''

# Commits on the connection to the database
conn.commit()

#######
# End SQL
#######

#print(armorDF.iloc[1,:])
#
#print(armorDF.iloc[:,1])
#
#len(armorDF)