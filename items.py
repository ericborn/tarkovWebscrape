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

webpage = requests.get('https://escapefromtarkov.fandom.com/wiki/Loot?action=edit&section=13')

# Decode the page
webpageSrc = webpage.content.decode('utf-8')

# conver the page to beautiful soup format
soup = bs(webpageSrc, 'lxml')

# converts textarea to a string
text = str(soup.textarea.contents[0])

# Grab item category
# create a while loop that iterates until it hits the third equal sign (=)
# then breaks. Add each letter in a variable then remove the first two items
# since they will be ==
equal_count = 0

item_cat = ''

i = 0

while equal_count < 3:
    if text[i] == '=':
        equal_count += 1
        item_cat = item_cat + str(text[i])
    else:
        item_cat = item_cat + str(text[i])
    i += 1

# remove first two and last characters since they are all equal signs
item_cat = item_cat[2:len(item_cat)-1]

# split text on |link=
item_split = text.split(r'|link=')

# setup then populate a list from the 0 element of each item in text_split
# which is split again on the first closed bracket symbol ]
item_list = []

for items in range(1, len(item_split)):
    item_list.append(item_split[items].split(r']')[0])

# TODO
# need to create a dataframe, store values from item_list then append
# the following types below

# other 
item_list[0:27]

# building materials
item_list[27:44]

# electronics
item_list[44:89]

# energy elements
item_list[89:97]

# Flammable materials
item_list[97:112]

# Household materials
item_list[112:129]

# medical supplies
item_list[129:140]

# tools
item_list[140:160]

# valuables
item_list[160:182]

# list got cut here for some reason, need to resolve as there are two more
# groups of items