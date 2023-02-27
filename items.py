# -*- coding: utf-8 -*-
"""
Created on Fri Feb 17 10:34:03 2023

@author: Eric
"""

import requests
from bs4 import BeautifulSoup as bs
import pandas as pd

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

# manually convert dogtag to BEAR and add USEC
loot_items[loot_items.index('Dogtag')] = 'BEAR Dogtag'
loot_items.insert(10, 'USEC Dogtag')

loot_items_2 = scrape_setup('https://escapefromtarkov.fandom.com/wiki/Loot?action=edit&section=12')
loot_items_3 = scrape_setup('https://escapefromtarkov.fandom.com/wiki/Loot?action=edit&section=13')

for item in loot_items_2:
    loot_items.append(item)

for item in loot_items_3:
    loot_items.append(item)    

item_category = 'Other'
item_type = 'Other'

# create a dataframe, store values from item_list then manually update
# types and categories
items_df = pd.DataFrame({'item_category': item_category,'item_name': loot_items, \
                         'type': item_type})

# set category to barter items
items_df['item_category'][0:183] = 'Barter Items'
    
# building materials
items_df['type'][28:45] = 'Building Materials'

# electronics
items_df['type'][45:90] = 'Electronics'

# energy elements
items_df['type'][90:98] = 'Energy Elements'

# Flammable materials
items_df['type'][98:113] = 'Flammable Materials'

# Household materials
items_df['type'][113:130] = 'Household Materials'

# medical supplies
items_df['type'][130:141] = 'Medical Supplies'

# tools
items_df['type'][141:161] = 'Tools'

# valuables
items_df['type'][161:183] = 'Valuables'

# info items
items_df['type'][183:198] = 'Info Items'
items_df['item_category'][183:198] = 'Info Items'

# special equipment
items_df['type'][198:] = 'Special Equipment'
items_df['item_category'][198:] = 'Special Equipment'

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

helmet_df['type'][0:2] = 'Headwear Mount'
helmet_df['type'][2:33] = 'Headwear Armored'
helmet_df['type'][33:] = 'Headwear Vanity'

# write df to csv
# helmet_df.to_csv('helmet.csv', index=False)

####
# end Helmet
####

####
# start secure container
####
secure_container = scrape_setup('https://escapefromtarkov.fandom.com/wiki/Secure_containers?action=edit')    

item_category = 'Gear'
item_type = 'Secure Container'

# create a dataframe, store values from item_list then manually update
# types and categories
secure_container_df = pd.DataFrame({'item_category': item_category,\
                           'item_name': secure_container, 'type': item_type})

# write df to csv
# secure_container_df.to_csv('secure_container.csv', index=False)

####
# end secure container
####

####
# start weapons
####

# primary
weap_list = [scrape_setup('https://escapefromtarkov.fandom.com/wiki/Weapons?action=edit&section=1')]

# secondary
weap_list.append(scrape_setup('https://escapefromtarkov.fandom.com/wiki/Weapons?action=edit&section=10'))

# special
weap_list.append(scrape_setup('https://escapefromtarkov.fandom.com/wiki/Weapons?action=edit&section=13'))

# melee
weap_list.append(scrape_setup('https://escapefromtarkov.fandom.com/wiki/Weapons?action=edit&section=19'))

# throwable
weap_list.append(scrape_setup('https://escapefromtarkov.fandom.com/wiki/Weapons?action=edit&section=20'))

# flatten list
weapons = [item for sublist in weap_list for item in sublist]

item_category = 'Weapon'
item_type = 'Assault Rifles'

# create a dataframe, store values from item_list then manually update
# types and categories
weapons_df = pd.DataFrame({'item_category': item_category,\
                           'item_name': weapons, 'type': item_type})

weapons_df['type'][0:32] = 'Assault Rifle'
weapons_df['type'][32:42] = 'Assault Carbine'
weapons_df['type'][42] = 'Light Machine Gun'
weapons_df['type'][43:62] = 'Submachine Gun'
weapons_df['type'][62:74] = 'Shotgun'
weapons_df['type'][74:81] = 'Designated Marksman Rifle'
weapons_df['type'][81:89] = 'Bolt Action Rifle'
weapons_df['type'][89:91] = 'Grenade Launcher'
weapons_df['type'][91:110] = 'Pistol'
weapons_df['type'][110:113] = 'Revolver'
weapons_df['type'][113] = 'Signal Pistol'
weapons_df['type'][114:118] = 'Handheld Flare'
weapons_df['type'][118:136] = 'Melee'
weapons_df['type'][136:143] = 'Fragmentation Grenade'
weapons_df['type'][143:145] = 'Smoke Grenade'
weapons_df['type'][145:] = 'Stun Grenade'

# write df to csv
# weapons_df.to_csv('weapons.csv', index=False)

####
# end weapons
####

####
# start money
####

# manually created since there are only 3
money_list = ['Dollar', 'Euro', 'Rouble']

item_category = 'Money'
item_type = 'Currency'

money_df = pd.DataFrame({'item_category': item_category,\
                         'item_name': money_list, 'type': item_type})

####
# end money
####

####
# start quest items
####

# manually created since there is not a dedicated page for all on the wiki
quest_item_list = ['Bronze Pocket Watch', 'Secure Folder 0022', 
                   'Secure Folder 0031', 'Military Documents 1',
                   'Military Documents 2', 'Military Documents 3',
                   'Sealed Letter', 'Bank Case' 'Registered Letter']

item_category = 'Quest'
item_type = 'Quest'

quest_item_df = pd.DataFrame({'item_category': item_category,\
                         'item_name': quest_item_list, 'type': item_type})

####
# end quest items
####

# ####
# # start actions
# # This is moved into its own table
# ####

# # manually created since there are only 3
# action_list = ['Eliminate', 'Find', 'Pick up', 'survive']

# item_category = 'Quest'
# item_type = 'Action'

# action_df = pd.DataFrame({'item_category': item_category,\
#                          'item_name': action_list, 'type': item_type})

# ####
# # end actions
# ####

####
# start secure container
####
gear_components = scrape_setup('https://escapefromtarkov.fandom.com/wiki/Gear_components?action=edit')    

item_category = 'Gear Component'
item_type = 'Gear'

# create a dataframe, store values from item_list then manually update
# types and categories
gear_components_df = pd.DataFrame({'item_category': item_category,\
                           'item_name': gear_components, 'type': item_type})

gear_components_df['type'][0:4] = 'Night Vision Device'
gear_components_df['type'][4] = 'Thermal Vision Device'
gear_components_df['type'][5] = 'Headset'
gear_components_df['type'][6:19] = 'Visor'
gear_components_df['type'][19:29] = 'Additional Armor'
gear_components_df['type'][29:35] = 'Mount'
gear_components_df['type'][35] = 'Vanity'

# write df to csv
# secure_container_df.to_csv('secure_container.csv', index=False)

####
# end secure container
####

####
# !!!TODO!!!
# ammo needs a recursive link crawler that drills into each ammo
# grabs all of the types along with ammo stats and is formatted into a DF
# start ammo
####

url_base = 'https://escapefromtarkov.fandom.com/wiki/'

header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.76",
    "X-Requested-With": "XMLHttpRequest"
}

url = 'https://escapefromtarkov.fandom.com/wiki/Ammunition'

# pull down the webpage
webpage = requests.get(url, headers=header)

# convert the html to a dataframe
web_df = pd.read_html(webpage.text, header = 0)

ammo_names = []

for df in range(0,6):
    ammo_names.append(list(web_df[df]['Name']))

# flatten list
ammo_link_names = [item for sublist in ammo_names for item in sublist]

# webpage = requests.get(url)

# # Decode the page
# webpageSrc = webpage.content.decode('utf-8')

# # conver the page to beautiful soup format
# soup = bs(webpageSrc, 'lxml')

# Creates an empty list to store all weapon main view page links
ammo_links = []

# replace spaces with underscore, append base URL to each ammo name
for ammo in range(len(ammo_link_names)):
    ammo_link_names[ammo] = ammo_link_names[ammo].replace(' ', '_')
    ammo_links.append(url_base + ammo_link_names[ammo])

# write df to csv
# secure_container_df.to_csv('secure_container.csv', index=False)

header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.76",
    "X-Requested-With": "XMLHttpRequest"
}

for url in ammo_links:
    # pull down the webpage
    webpage = requests.get(url, headers=header)
    
    # convert the html to a dataframe
    web_df = pd.read_html(webpage.text, header = 0)
    
    # create a list of column names
    column_list = list(web_df[0].columns)
    
    # remove the first and last elements from the list
    column_list.pop(0)
    column_list.pop(-1)
    
    # create a dataframe containing just the ammo stats
    ammo_df = web_df[0][column_list]
    
    # pull down the webpage
    webpage = requests.get(ammo_links[1], headers=header)
    
    # convert the html to a dataframe
    web_df = pd.read_html(webpage.text, header = 0)
    
    # create a list of column names
    column_list = list(web_df[0].columns)
    
    # remove the first and last elements from the list
    column_list.pop(0)
    column_list.pop(-1)
    
    # create a dataframe containing just the ammo stats
    ammo_df_1 = web_df[0][column_list]
    
    ammo_df.merge(ammo_df_1, how='outer')
    
    
    item_category = 'Ammo'
    item_type = 'Secure Container'
    
    # create a dataframe, store values from item_list then manually update
    # types and categories
    ammo_df = pd.DataFrame({'item_category': item_category,\
                                'item_name': ammo, 'type': item_type})



####
# end ammo
####

####
# !!!TODO!!!
# Weapon mods needs a recursive link crawler that drills into each mod
# grabs all of the types along with stats and is formatted into a DF
# start weapon mods
####
# weap_mods = scrape_setup('https://escapefromtarkov.fandom.com/wiki/Weapon_mods')    

# item_category = 'Weapon Mod'
# item_type = 'Functional Mod'

# # create a dataframe, store values from item_list then manually update
# # types and categories
# weap_mods_df = pd.DataFrame({'item_category': item_category,\
#                            'item_name': weap_mods, 'type': item_type})

# # write df to csv
# # weap_mods_df.to_csv('weapon_mods.csv', index=False)

####
# end weapon mods
####

####
# combine and output
####


all_dataframes = [items_df, medical_df, provision_df, key_df, armbands_df, 
                  armor_vest_df, backpack_df, rig_df, eyewear_df,face_cover_df,
                  headset_df, helmet_df, secure_container_df, weapons_df, 
                  money_df, quest_item_df, gear_components_df]

all_items_df = pd.concat(all_dataframes)

# write df to csv
all_items_df.to_csv('items.csv', index=False)