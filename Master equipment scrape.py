# -*- coding: utf-8 -*-
"""
Created on Tue Jul  9 18:40:52 2019

@author: Eric Born
"""
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import re
import time

armorCols = ['itemtypeid','slotid','weight','gridsize','price','traderid','rarity', 'material', 'armor', 'armorcoverage',
             'armorsegments', 'durability', 'ricochetchance', 'penalties','blocksarmor', 'blocksearpiece', 'blockseyewear', 
             'blocksfacecover','blocksheadwear','slots','name']

# body armor
armorPage = requests.get('https://escapefromtarkov.gamepedia.com/Armor_vests')

# rigs
rigPage = requests.get('https://escapefromtarkov.gamepedia.com/Chest_rigs')

# helmet
helmetPage = requests.get('https://escapefromtarkov.gamepedia.com/Helmet')

# backpack
backpackPage = requests.get('https://escapefromtarkov.gamepedia.com/Backpacks')

# Earpieces
earpiecePage = requests.get('https://escapefromtarkov.gamepedia.com/Earpieces')

# Headwear
HeadwearPage = requests.get('https://escapefromtarkov.gamepedia.com/Headwear')

siteList = [requests.get('https://escapefromtarkov.gamepedia.com/Armor_vests'), 
            requests.get('https://escapefromtarkov.gamepedia.com/Chest_rigs'),
            requests.get('https://escapefromtarkov.gamepedia.com/Helmet')]