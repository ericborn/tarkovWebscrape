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

webpage = requests.get('https://escapefromtarkov.fandom.com/wiki/Loot?action=edit&section=2')

# Decode the page
webpageSrc = webpage.content.decode('utf-8')

# conver the page to beautiful soup format
soup = bs(webpageSrc, 'lxml')

# converts textarea to a string
text = str(soup.textarea.contents[0])

# not used since there are 3 categories they're manually being set
# # Grab item category
# # create a while loop that iterates until it hits the third equal sign (=)
# # then breaks. Add each letter in a variable then remove the first two items
# # since they will be ==
# equal_count = 0

# item_cat = ''

# i = 0

# while equal_count < 3:
#     if text[i] == '=':
#         equal_count += 1
#         item_cat = item_cat + str(text[i])
#     else:
#         item_cat = item_cat + str(text[i])
#     i += 1

# # remove first two and last characters since they are all equal signs
# item_cat = item_cat[2:len(item_cat)-1]

# split text on |link=
item_split = text.split(r'|link=')

# setup then populate a list from the 0 element of each item in text_split
# which is split again on the first closed bracket symbol ]
item_list = []

for items in range(1, len(item_split)):
    item_list.append(item_split[items].split(r']')[0])

# list got cut here for some reason so repeating second and third converts to list
# start info items
webpage = requests.get('https://escapefromtarkov.fandom.com/wiki/Loot?action=edit&section=12')

# Decode the page
webpageSrc = webpage.content.decode('utf-8')

# conver the page to beautiful soup format
soup = bs(webpageSrc, 'lxml')

# converts textarea to a string
text = str(soup.textarea.contents[0])

# # Grab item category
# # create a while loop that iterates until it hits the third equal sign (=)
# # then breaks. Add each letter in a variable then remove the first two items
# # since they will be ==
# equal_count = 0

# item_cat = ''

# i = 0

# while equal_count < 3:
#     if text[i] == '=':
#         equal_count += 1
#         item_cat = item_cat + str(text[i])
#     else:
#         item_cat = item_cat + str(text[i])
#     i += 1

# # remove first two and last characters since they are all equal signs
# item_cat = item_cat[2:len(item_cat)-1]

# split text on |link=
item_split = text.split(r'|link=')

for items in range(1, len(item_split)):
    item_list.append(item_split[items].split(r']')[0])

# start info items
webpage = requests.get('https://escapefromtarkov.fandom.com/wiki/Loot?action=edit&section=13')

# Decode the page
webpageSrc = webpage.content.decode('utf-8')

# conver the page to beautiful soup format
soup = bs(webpageSrc, 'lxml')

# converts textarea to a string
text = str(soup.textarea.contents[0])

# # Grab item category
# # create a while loop that iterates until it hits the third equal sign (=)
# # then breaks. Add each letter in a variable then remove the first two items
# # since they will be ==
# equal_count = 0

# item_cat = ''

# i = 0

# while equal_count < 3:
#     if text[i] == '=':
#         equal_count += 1
#         item_cat = item_cat + str(text[i])
#     else:
#         item_cat = item_cat + str(text[i])
#     i += 1

# # remove first two and last characters since they are all equal signs
# item_cat = item_cat[2:len(item_cat)-1]

# split text on |link=
item_split = text.split(r'|link=')

for items in range(1, len(item_split)):
    item_list.append(item_split[items].split(r']')[0])


# create a dataframe, store values from item_list then append
# the following types below

items_df = pd.DataFrame({'item_category': 'other','item_name': item_list, \
                         'type': 'other'})

# set category to barter items
items_df['item_category'][0:182] = 'barter items'
    
# building materials
items_df['type'][27:44] = 'building materials'

# electronics
items_df['type'][44:89] = 'electronics'

# energy elements
items_df['type'][89:97] = 'energy elements'

# Flammable materials
items_df['type'][97:112] = 'flammable materials'

# Household materials
items_df['type'][112:129] = 'household materials'

# medical supplies
items_df['type'][129:140] = 'medical supplies'

# tools
items_df['type'][140:160] = 'tools'

# valuables
items_df['type'][160:182] = 'valuables'

# info items
items_df['type'][182:197] = 'info items'
items_df['item_category'][182:197] = 'info items'

# special equipment
items_df['type'][197:207] = 'special equipment'
items_df['item_category'][197:207] = 'special equipment'

# write df to csv
items_df.to_csv(index=False)