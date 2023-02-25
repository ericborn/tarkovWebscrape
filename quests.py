# -*- coding: utf-8 -*-
"""
Created on Fri Feb 24 18:34:19 2023

@author: Eric

trader list

0 Unknown
1 Therapist
2 Prapor
3 Skier
4 Peacekeeper
5 Mechanic
6 Ragman
7 Jaeger
8 Fence
9 Lightkeeper
"""

import requests
from bs4 import BeautifulSoup as bs
import pandas as pd

# get webpage
webpage = requests.get('https://escapefromtarkov.fandom.com/wiki/Quests?action=edit&section=3')

# Decode the page
webpageSrc = webpage.content.decode('utf-8')

# conver the page to beautiful soup format
soup = bs(webpageSrc, 'lxml')

# converts textarea to a string
text = str(soup.textarea.contents[0])

# split text on |link=
quest_split = text.split(r"'''[[")

# create and populate a list of items
quest_list = []

for quest in range(1, len(quest_split)):
    quest_list.append(quest_split[quest].split(r']')[0])

quest_giver = '0'
quest_type = 'Other'

# create a dataframe, store values from item_list then manually update
# types and categories
quest_df = pd.DataFrame({'quest_giver': quest_giver,'quest_name': quest_list, \
                         'type': quest_type})

# set quest giver
quest_df['quest_giver'][0:43] = '2'
quest_df['quest_giver'][43:77] = '1'
quest_df['quest_giver'][77:109] = '3'
quest_df['quest_giver'][109:156] = '4'
quest_df['quest_giver'][156:218] = '5'
quest_df['quest_giver'][218:254] = '6'
quest_df['quest_giver'][254:308] = '7'
quest_df['quest_giver'][308:316] = '8'
quest_df['quest_giver'][316:] = '9'

# delete rows 0, 43, 77, 109-112, 155, 218, 254-257, 308, 316-317
# rows contain quest giver name or pre-req to access trader
quest_df = quest_df.drop(quest_df.index[[0, 43, 77, 109, 110, 111, 112, 155, 218, 254, 255, 256, 257, 308, 316, 317]])

# reset index just in case
quest_df.reset_index(drop=True, inplace=True)

# write df to csv
quest_df.to_csv('quests.csv', index=False)