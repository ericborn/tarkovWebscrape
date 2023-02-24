# -*- coding: utf-8 -*-
"""
Created on Fri Feb 17 10:34:03 2023

@author: Eric
"""

import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import re
import time



def scrape_setup(url):
    # get webpage
    webpage = requests.get(url)

    # Decode the page
    webpageSrc = webpage.content.decode('utf-8')

    # conver the page to beautiful soup format
    soup = bs(webpageSrc, 'lxml')

    # converts textarea to a string
    text = str(soup.textarea.contents[0])
    
    # split text on |link=
    item_split = text.split(r'|link=')
    
    # create and populate a list of items
    item_list = []
    
    for items in range(1, len(item_split)):
        item_list.append(item_split[items].split(r']')[0])
        
    return(item_list)


loot_items = scrape_setup('https://escapefromtarkov.fandom.com/wiki/Loot?action=edit&section=2')
loot_items_2 = scrape_setup('https://escapefromtarkov.fandom.com/wiki/Loot?action=edit&section=12')
loot_items_3 = scrape_setup('https://escapefromtarkov.fandom.com/wiki/Loot?action=edit&section=13')

for item in loot_items_2:
    loot_items.append(item)

for item in loot_items_3:
    loot_items.append(item)    

item_category = 'other'
item_type = 'other'

# create a dataframe, store values from item_list then manually update
# types and categories
items_df = pd.DataFrame({'item_category': item_category,'item_name': loot_items, \
                         'type': item_type})

# set category to barter items
items_df['item_category'][0:182] = 'Barter Items'
    
# building materials
items_df['type'][27:44] = 'Building Materials'

# electronics
items_df['type'][44:89] = 'Electronics'

# energy elements
items_df['type'][89:97] = 'Energy Elements'

# Flammable materials
items_df['type'][97:112] = 'Flammable Materials'

# Household materials
items_df['type'][112:129] = 'Household Materials'

# medical supplies
items_df['type'][129:140] = 'Medical Supplies'

# tools
items_df['type'][140:160] = 'Tools'

# valuables
items_df['type'][160:182] = 'Valuables'

# info items
items_df['type'][182:197] = 'Info Items'
items_df['item_category'][182:197] = 'Info Items'

# special equipment
items_df['type'][197:207] = 'Special Equipment'
items_df['item_category'][197:207] = 'Special Equipment'

# write df to csv
# items_df.to_csv('items.csv', index=False)

####
# start med items
####
medical_items = scrape_setup('https://escapefromtarkov.fandom.com/wiki/Medical?action=edit&section=1')    

item_category = 'Medical Items'
item_type = 'other'

# create a dataframe, store values from item_list then manually update
# types and categories
medical_df = pd.DataFrame({'item_category': item_category,\
                           'item_name': medical_items, 'type': item_type})
    
# Drugs
medical_df['type'][0:5] = 'Drug'

# Injury Treatments
medical_df['type'][5:14] = 'Injury Treatment'

# Medikits
medical_df['type'][14:] = 'Medikit'

# write df to csv
# medical_df.to_csv('medical.csv', index=False)

####
# end med items
####

####
# start provisions
####
provision_items = scrape_setup('https://escapefromtarkov.fandom.com/wiki/Provisions?action=edit')    

item_category = 'Provisions'
item_type = 'other'

# create a dataframe, store values from item_list then manually update
# types and categories
provision_df = pd.DataFrame({'item_category': item_category,\
                           'item_name': provision_items, 'type': item_type})
    
# Food
provision_df['type'][0:20] = 'Food'

# Drink
provision_df['type'][20:] = 'Drink'

# write df to csv
# provision_df.to_csv('provisions.csv', index=False)

####
# end provisions
####

####
# start keys
####
keys = scrape_setup('https://escapefromtarkov.fandom.com/wiki/Keys_%26_Intel?action=edit')    

item_category = 'Keys'
item_type = 'other'

# create a dataframe, store values from item_list then manually update
# types and categories
key_df = pd.DataFrame({'item_category': item_category,\
                           'item_name': keys, 'type': item_type})
    
# key
key_df['type'][0:93] = 'Key'
key_df['type'][106:] = 'Key'

# card
key_df['type'][93:106] = 'Card'

# write df to csv
# key_df.to_csv('keys.csv', index=False)

####
# end keys
####

####
# start armbands
####
armbands = scrape_setup('https://escapefromtarkov.fandom.com/wiki/Armbands?action=edit')    

item_category = 'Gear'
item_type = 'Armbands'

# create a dataframe, store values from item_list then manually update
# types and categories
armbands_df = pd.DataFrame({'item_category': item_category,\
                           'item_name': armbands, 'type': item_type})

# write df to csv
# armbands_df.to_csv('armbands.csv', index=False)

####
# end armbands
####

####
# start armored vests
####
armor_vest = scrape_setup('https://escapefromtarkov.fandom.com/wiki/Armor_vests?action=edit')    

item_category = 'Gear'
item_type = 'Armored Vest'

# create a dataframe, store values from item_list then manually update
# types and categories
armor_vest_df = pd.DataFrame({'item_category': item_category,\
                           'item_name': armor_vest, 'type': item_type})

# write df to csv
# armor_vest_df.to_csv('armor_vest.csv', index=False)

####
# end armored vests
####

####
# start backpacks
####
backpack = scrape_setup('https://escapefromtarkov.fandom.com/wiki/Backpacks?action=edit')    

item_category = 'Gear'
item_type = 'Backpack'

# create a dataframe, store values from item_list then manually update
# types and categories
backpack_df = pd.DataFrame({'item_category': item_category,\
                           'item_name': backpack, 'type': item_type})

# write df to csv
# backpack_df.to_csv('backpack.csv', index=False)

####
# end backpacks
####

####
# start rigs
####
rig = scrape_setup('https://escapefromtarkov.fandom.com/wiki/Chest_rigs?action=edit')    

item_category = 'Gear'
item_type = 'Chest Rig'

# create a dataframe, store values from item_list then manually update
# types and categories
rig_df = pd.DataFrame({'item_category': item_category,\
                           'item_name': rig, 'type': item_type})

rig_df['type'][0:21] = 'Armored Chest Rig'
rig_df['type'][21:] = 'Unarmored Chest Rig'

# write df to csv
# rig_df.to_csv('rig.csv', index=False)

####
# end rigs
####

####
# start eyewear
####
eyewear = scrape_setup('https://escapefromtarkov.fandom.com/wiki/Eyewear?action=edit')    

item_category = 'Gear'
item_type = 'Eyewear'

# create a dataframe, store values from item_list then manually update
# types and categories
eyewear_df = pd.DataFrame({'item_category': item_category,\
                           'item_name': eyewear, 'type': item_type})

eyewear_df['type'][0:2] = 'Armored Eyewear'
eyewear_df['type'][2:] = 'Unarmored Eyewear'

# write df to csv
# eyewear_df.to_csv('eyewear.csv', index=False)

####
# end eyewear
####

####
# start face cover
####
face_cover = scrape_setup('https://escapefromtarkov.fandom.com/wiki/Face_cover?action=edit')    

item_category = 'Gear'
item_type = 'Face Cover'

# create a dataframe, store values from item_list then manually update
# types and categories
face_cover_df = pd.DataFrame({'item_category': item_category,\
                           'item_name': face_cover, 'type': item_type})

face_cover_df['type'][0:5] = 'Armored Face Cover'
face_cover_df['type'][5:] = 'Unarmored Face Cover'

# write df to csv
# face_cover_df.to_csv('face_cover.csv', index=False)

####
# end face cover
####

####
# start headset
####
headset = scrape_setup('https://escapefromtarkov.fandom.com/wiki/Headsets?action=edit')    

item_category = 'Gear'
item_type = 'Headset'

# create a dataframe, store values from item_list then manually update
# types and categories
headset_df = pd.DataFrame({'item_category': item_category,\
                           'item_name': headset, 'type': item_type})

# write df to csv
# headset_df.to_csv('headset.csv', index=False)

####
# end headset
####

####
# start Helmet
####
helmet = scrape_setup('https://escapefromtarkov.fandom.com/wiki/Headwear?action=edit')    

item_category = 'Gear'
item_type = 'Headwear'

# create a dataframe, store values from item_list then manually update
# types and categories
helmet_df = pd.DataFrame({'item_category': item_category,\
                           'item_name': helmet, 'type': item_type})

helmet_df['type'][0:2] = 'Mount'
helmet_df['type'][2:33] = 'Armored Helmet'
helmet_df['type'][33:] = 'Vanity'

# write df to csv
# face_cover_df.to_csv('helmet.csv', index=False)

####
# end Helmet
####