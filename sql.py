# -*- coding: utf-8 -*-
"""
Created on Sun Jul  7 17:31:06 2019

@author: Eric Born
"""
from sqlalchemy import create_engine, MetaData, insert, Table, Column, String, Integer, Float, Boolean
meta = MetaData()

engine = create_engine('postgresql://TomBrody:pass@localhost/tarkov')

currency = Table('currency', meta,
                 Column('currId', Integer(), primary_key = True, unique = True),
                 Column('currType', String(20)),
)

meta.create_all(engine)

print(engine.table_names())